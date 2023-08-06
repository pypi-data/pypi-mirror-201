import datetime
import json
import logging
import sys
import os
import time
import socket

DIR = os.path.dirname(os.path.realpath(__file__))
path = f"{os.path.dirname(DIR)}"
temp_path = [path]
temp_path.extend(sys.path)
sys.path = temp_path


import influxdb_datalogger

logger = logging.getLogger("pytest")

DATA_FILE = f"{DIR}/data-file.json"
EVENT_FILE = f"{DIR}/event-file.json"


class DbWriter(influxdb_datalogger.DatabaseWriter):
    def write_data(self, datalogger: influxdb_datalogger.DataLogger):
        dataset = datalogger.dataset
        if os.path.exists(DATA_FILE):
            # If the file exists we are probably writing more than once in a test.
            # Since DbWriter just writes to a JSON file we need to essentially append to the existing data, which is what this does.

            loaded_dataset = json.load(open(DATA_FILE))
            dataset = [*loaded_dataset, *dataset]
        json.dump(dataset, open(DATA_FILE, "w"), indent=2)


class GrafanaEventWriter(influxdb_datalogger.DatabaseWriter):
    def write_data(self, datalogger: influxdb_datalogger.DataLogger):
        events = datalogger.events
        events_to_write = list()
        for event in events:
            event: influxdb_datalogger.datalogger.Event
            marker_data = dict(time=int(event.start * 1000), timeEnd=int(event.stop * 1000), tags=event.tags_map, text=event.measurement)
            events_to_write.append(marker_data)

        if os.path.exists(EVENT_FILE):
            # If the file exists we are probably writing more than once in a test.
            # Since DbWriter just writes to a JSON file we need to essentially append to the existing data, which is what this does.

            loaded_events = json.load(open(EVENT_FILE))
            events_to_write = [*loaded_events, *events_to_write]
        json.dump(events_to_write, open(EVENT_FILE, "w"), indent=2)


class TestDatalogger:

    ############################################################################################################
    # Setup/teardown
    ############################################################################################################

    def setup_method(self):
        self.remove_data_file()
        self.remove_events_file()

    def teardown_method(self):
        self.remove_data_file()
        self.remove_events_file()

    ############################################################################################################
    # Functions
    ############################################################################################################

    def remove_data_file(self):
        try:
            os.remove(DATA_FILE)
        except:
            # Probably doesn't exist; this is fine
            pass

    def remove_events_file(self):
        try:
            os.remove(EVENT_FILE)
        except:
            # Probably doesn't exist; this is fine
            pass

    def assert_data_file_doesnt_exist(self):
        assert not os.path.exists(DATA_FILE), f"File {DATA_FILE} exists when it shouldn't at this point"

    def assert_event_file_doesnt_exist(self):
        assert not os.path.exists(EVENT_FILE), f"File {EVENT_FILE} exists when it shouldn't at this point"

    def load_dataset_from_data_file(self):
        return json.load(open(DATA_FILE))

    def load_events_from_event_file(self):
        return json.load(open(EVENT_FILE))

    ############################################################################################################
    # Tests
    ############################################################################################################

    def test_field_map(self):
        f = influxdb_datalogger.Field("duration")
        fm = influxdb_datalogger.FieldMap.build(f, 2)

        assert f in fm
        assert fm[f] == 2

    def test_field_map_fail(self):
        try:
            fm = influxdb_datalogger.FieldMap.build(influxdb_datalogger.Tag("duration"), 2)
            raise Exception("Managed to create a FieldMap that should not be possible to create")
        except:
            logger.info("Correctly failed to create a map that should not be possible to make")

    def test_tags_map(self):
        t = influxdb_datalogger.Tag("name")
        tm = influxdb_datalogger.TagMap.build(t, "testing")

        assert t in tm
        assert tm[t] == "testing"

    def test_tags_map_fail(self):
        try:
            tm = influxdb_datalogger.TagMap.build(influxdb_datalogger.Field("duration"), 2)
            raise Exception("Managed to create a TagMap that should not be possible to create")
        except:
            logger.info("Correctly failed to create a map that should not be possible to make")

    def test_block_measure(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        m = influxdb_datalogger.Measurement("time-taken", f, t)
        tm = influxdb_datalogger.TagMap.build(t, "test")
        datalogger = influxdb_datalogger.DataLogger(DbWriter())
        with datalogger.measure_block(m, f, tm):
            logger.info(f"Taking measurement {m}")

        assert m in datalogger._dataset, f"Measurement {m} not in the dataset"

    def test_write_data(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        m = influxdb_datalogger.Measurement("time-taken", f, t)
        tm = influxdb_datalogger.TagMap.build(t, "test")
        datalogger = influxdb_datalogger.DataLogger(DbWriter())
        with datalogger.measure_block(m, f, tm):
            logger.info(f"Taking measurement {m}")

        assert m in datalogger._dataset, f"Measurement {m} not in the dataset"
        self.assert_data_file_doesnt_exist()

        datalogger.write_data()
        loaded_dataset = self.load_dataset_from_data_file()
        logger.info(loaded_dataset)
        assert len(loaded_dataset) == 1, f"Unexpected: {loaded_dataset}"

    def test_measure_wrapper(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        m = influxdb_datalogger.Measurement("time-taken", f, t)
        tm = influxdb_datalogger.TagMap.build(t, "test")
        datalogger = influxdb_datalogger.DataLogger(DbWriter())

        def runner(arg1):
            logger.info(f"Taking measurement {m}: {arg1}")

        datalogger.measure(func=runner,
                           measurement=m,
                           field=f,
                           tags_map=tm,
                           logger=logger,
                           log_start=f"Starting {runner.__name__}",
                           log_end=f"Finished {runner.__name__}",
                           args=("test",))

        assert m in datalogger._dataset, f"Measurement {m} not in the dataset"

    def test_post_processing(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        m = influxdb_datalogger.Measurement("time-taken", f, t)
        tm = influxdb_datalogger.TagMap.build(t, "test")
        datalogger = influxdb_datalogger.DataLogger(DbWriter())
        epoch = time.time()

        @influxdb_datalogger.PostProcessing.register(m)
        def validate_post_processing(datalogger: influxdb_datalogger.DataLogger, **kwargs):
            logger.info(datalogger)
            logger.info(kwargs)
            datalogger.log(m, influxdb_datalogger.FieldMap.build(f, epoch), influxdb_datalogger.TagMap.build(t, "post"))

        datalogger.add_post_processing(validate_post_processing)

        with datalogger.measure_block(m, f, tm):
            logger.info(f"Taking measurement {m}")

        self.assert_data_file_doesnt_exist()

        datalogger.write_data()
        loaded_dataset = self.load_dataset_from_data_file()
        logger.info(loaded_dataset)
        assert len(loaded_dataset) == 2, f"Unexpected: {loaded_dataset}"
        assert loaded_dataset[0]["measurement"] == m, f"Unexpected: {loaded_dataset}"
        assert loaded_dataset[1]["measurement"] == m, f"Unexpected: {loaded_dataset}"
        assert loaded_dataset[1]["fields"][f] == epoch, f"Unexpected: {loaded_dataset}"

    def test_continuous_write(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        m = influxdb_datalogger.Measurement("time-taken", f, t)
        datalogger = influxdb_datalogger.DataLogger(DbWriter(), continuous_write=True)

        with datalogger.measure_block(m, f, influxdb_datalogger.TagMap.build(t, "first")):
            logger.info(f"Taking first measurement and doing an immediate write {m}")

        with datalogger.measure_block(m, f, influxdb_datalogger.TagMap.build(t, "second")):
            logger.info(f"Taking second measurement and doing an immediate write {m}")

        # NOTE: We do a continuous write, which means there's nothing in the dataset because
        # the dataset is wiped when writing the data since we don't want to write duplicates

        loaded_dataset = self.load_dataset_from_data_file()
        logger.info(loaded_dataset)
        assert len(loaded_dataset) == 2, f"Unexpected: {loaded_dataset}"
        assert loaded_dataset[0]["tags"][t] == "first", f"Unexpected: {loaded_dataset}"
        assert loaded_dataset[1]["tags"][t] == "second", f"Unexpected: {loaded_dataset}"

    def test_events(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        h = influxdb_datalogger.Tag("hostname")

        m = influxdb_datalogger.Measurement("time-taken", f, t)
        etm = influxdb_datalogger.TagMap.build(h, socket.gethostname())

        datalogger = influxdb_datalogger.DataLogger(DbWriter(), GrafanaEventWriter())

        with datalogger.measure_block(m, f, influxdb_datalogger.TagMap.build(t, "first"), event_tags=etm):
            logger.info(f"Taking first measurement and logging events {m}")

        with datalogger.measure_block(m, f, influxdb_datalogger.TagMap.build(t, "second"), event_tags=etm):
            logger.info(f"Taking second measurement and logging events {m}")

        with datalogger.measure_block(m, f, influxdb_datalogger.TagMap.build(t, "third")):
            logger.info(f"Taking third measurement and NOT logging events {m}")

        self.assert_event_file_doesnt_exist()

        datalogger.write_data()

        loaded_events = self.load_events_from_event_file()
        logger.info(loaded_events)
        assert len(loaded_events) == 2

    def test_events_continuous_write(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        h = influxdb_datalogger.Tag("hostname")

        m = influxdb_datalogger.Measurement("time-taken", f, t)
        etm = influxdb_datalogger.TagMap.build(h, socket.gethostname())

        datalogger = influxdb_datalogger.DataLogger(DbWriter(), GrafanaEventWriter(), continuous_write=True)

        with datalogger.measure_block(m, f, influxdb_datalogger.TagMap.build(t, "first"), event_tags=etm):
            logger.info(f"Taking first measurement and logging events {m}")

        loaded_events = self.load_events_from_event_file()
        assert len(loaded_events) == 1

        with datalogger.measure_block(m, f, influxdb_datalogger.TagMap.build(t, "second"), event_tags=etm):
            logger.info(f"Taking second measurement and logging events {m}")

        loaded_events = self.load_events_from_event_file()
        assert len(loaded_events) == 2

        with datalogger.measure_block(m, f, influxdb_datalogger.TagMap.build(t, "third")):
            logger.info(f"Taking third measurement and NOT logging events {m}")

        loaded_events = self.load_events_from_event_file()
        assert len(loaded_events) == 2

    def test_events_continuous_write_measure(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        h = influxdb_datalogger.Tag("hostname")

        m = influxdb_datalogger.Measurement("time-taken", f, t)
        etm = influxdb_datalogger.TagMap.build(h, socket.gethostname())

        datalogger = influxdb_datalogger.DataLogger(DbWriter(), GrafanaEventWriter(), continuous_write=True)

        def runner(arg1):
            logger.info(f"Taking measurement {m}: {arg1}")

        datalogger.measure(func=runner,
                           measurement=m,
                           field=f,
                           tags_map=influxdb_datalogger.TagMap.build(t, "first"),
                           logger=logger,
                           log_start=f"Starting {runner.__name__}",
                           log_end=f"Finished {runner.__name__}",
                           event_tags=etm,
                           args=("first",))

        loaded_events = self.load_events_from_event_file()
        assert len(loaded_events) == 1

        datalogger.measure(func=runner,
                           measurement=m,
                           field=f,
                           tags_map=influxdb_datalogger.TagMap.build(t, "second"),
                           logger=logger,
                           log_start=f"Starting {runner.__name__}",
                           log_end=f"Finished {runner.__name__}",
                           event_tags=etm,
                           args=("second",))

        loaded_events = self.load_events_from_event_file()
        assert len(loaded_events) == 2

        datalogger.measure(func=runner,
                           measurement=m,
                           field=f,
                           tags_map=influxdb_datalogger.TagMap.build(t, "third"),
                           logger=logger,
                           log_start=f"Starting {runner.__name__}",
                           log_end=f"Finished {runner.__name__}",
                           args=("third",))

        loaded_events = self.load_events_from_event_file()
        assert len(loaded_events) == 2

    def test_default_tags(self):
        def get_hostname():
            return socket.gethostname()
        f = influxdb_datalogger.Field("duration")
        h = influxdb_datalogger.Tag("hostname", func=get_hostname)
        m = influxdb_datalogger.Measurement("time-taken", f, h)

        datalogger = influxdb_datalogger.DataLogger(DbWriter(), GrafanaEventWriter())

        with datalogger.measure_block(m, f):
            logger.info(f"Should log a default value for tag {h}")

        datalogger.write_data()

        dataset = self.load_dataset_from_data_file()
        logger.info(dataset)
        assert h in dataset[0]["tags"]

    def test_default_fields(self):
        def get_hostname():
            return socket.gethostname()
        f = influxdb_datalogger.Field("duration")
        h = influxdb_datalogger.Field("hostname", func=get_hostname)
        m = influxdb_datalogger.Measurement("time-taken", f, h)

        datalogger = influxdb_datalogger.DataLogger(DbWriter(), GrafanaEventWriter())

        with datalogger.measure_block(m, f):
            logger.info(f"Should log a default value for field {h}")

        datalogger.write_data()

        dataset = self.load_dataset_from_data_file()
        logger.info(dataset)
        assert h in dataset[0]["fields"]

    def test_tag_map_copy(self):
        t = time.time()
        time_tag = influxdb_datalogger.Tag("time")
        tm = influxdb_datalogger.TagMap.build(influxdb_datalogger.Tag("host"), "https://host.com")
        tm_copy = tm.copy()
        assert isinstance(tm_copy, influxdb_datalogger.TagMap)
        tm_copy.add(time_tag, t)
        assert time_tag not in tm

    def test_field_map_copy(self):
        t = time.time()
        time_field = influxdb_datalogger.Field("time")
        fm = influxdb_datalogger.FieldMap.build(influxdb_datalogger.Field("duration"), 3.14)
        fm_copy = fm.copy()
        assert isinstance(fm_copy, influxdb_datalogger.FieldMap)
        fm_copy.add(time_field, t)
        assert time_field not in fm

    def test_block_measurement_with_logging(self):

        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        m = influxdb_datalogger.Measurement("time-taken", f, t)
        tm = influxdb_datalogger.TagMap.build(t, "test")
        datalogger = influxdb_datalogger.DataLogger(DbWriter())
        with datalogger.measure_block(m, f, tm, logger=logger, log_start="Starting", log_end="Done"):
            logger.info(f"Taking measurement {m}")

        assert m in datalogger._dataset, f"Measurement {m} not in the dataset"

        datalogger = influxdb_datalogger.DataLogger(DbWriter())
        with influxdb_datalogger.BlockMeasurer(datalogger, m, f, tm, logger=logger, log_start="Starting", log_end="Done"):
            logger.info("Taking measurement again")

    def test_last_data_entry(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        m = influxdb_datalogger.Measurement("time-taken", f, t)
        tm_1 = influxdb_datalogger.TagMap.build(t, "test_1")
        tm_2 = influxdb_datalogger.TagMap.build(t, "test_2")
        datalogger = influxdb_datalogger.DataLogger(DbWriter())
        with datalogger.measure_block(m, f, tm_1, logger=logger, log_start="Starting", log_end="Done"):
            logger.info(f"Taking measurement {m}")

        with datalogger.measure_block(m, f, tm_2, logger=logger, log_start="Starting", log_end="Done"):
            logger.info(f"Taking measurement {m}")

        last: influxdb_datalogger.DataEntry = datalogger.last_data_entry
        assert last.measurement == m
        assert last.tags == tm_2
        assert f.field_name in last.fields

    def test_last_event(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        m = influxdb_datalogger.Measurement("time-taken", f, t)
        tm_1 = influxdb_datalogger.TagMap.build(t, "test_1")
        tm_2 = influxdb_datalogger.TagMap.build(t, "test_2")
        datalogger = influxdb_datalogger.DataLogger(DbWriter(), GrafanaEventWriter())
        with datalogger.measure_block(m, f, tm_1, logger=logger, log_start="Starting", log_end="Done", event_tags=influxdb_datalogger.TagMap.build(t, "event-1")):
            logger.info(f"Taking measurement {m}")

        with datalogger.measure_block(m, f, tm_2, logger=logger, log_start="Starting", log_end="Done", event_tags=influxdb_datalogger.TagMap.build(t, "event-2")):
            logger.info(f"Taking measurement {m}")

        last: influxdb_datalogger.Event = datalogger.last_event
        assert last.measurement == m
        assert last.tags_map[t] == "event-2"

    def test_descriptions(self):
        f = influxdb_datalogger.Field("duration", desc="Field used for the measurement")
        t = influxdb_datalogger.Tag("identifier", desc="Tag used for the measurement")
        m = influxdb_datalogger.Measurement("time-taken", f, t, desc="Measurement used for the test")

        assert f.desc == "Field used for the measurement", f"Field description is {f.desc}"
        assert t.desc == "Tag used for the measurement", f"Tag description is {t.desc}"
        assert m.desc == "Measurement used for the test", f"Description is {m.desc}"

    def test_time_override(self):
        f = influxdb_datalogger.Field("duration")
        t = influxdb_datalogger.Tag("identifier")
        m = influxdb_datalogger.Measurement("time-taken", f, t)
        tm_1 = influxdb_datalogger.TagMap.build(t, "test_1")
        datalogger = influxdb_datalogger.DataLogger(DbWriter())
        now = datetime.datetime.utcnow()
        datalogger.log(m, influxdb_datalogger.FieldMap.build(f, 1.0), tm_1, time=now)
        assert datalogger.last_data_entry.time == str(now), f"Time is {datalogger.last_data_entry.time}"

        datalogger.log(m, influxdb_datalogger.FieldMap.build(f, 2.0), tm_1)
        logger.info(f"Time is {datalogger.last_data_entry.time}")
        assert datalogger.last_data_entry.time != str(now) and datetime.datetime.fromisoformat(datalogger.last_data_entry.time), f"Time is {datalogger.last_data_entry.time}"

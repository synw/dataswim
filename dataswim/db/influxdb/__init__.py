from influxdb import DataFrameClient


class InfluxDb():
    """
    A class to handle InfluxDb database
    """

    def __init__(self):
        """
        Initialize
        """
        self.influx_cli = None

    def influx_init(self, url, port, user, pwd, db):
        """
        Initialize an Influxdb database client
        """
        try:
            cli = DataFrameClient(url, port, user, pwd, db)
            self.influx_cli = cli
        except Exception as e:
            self.err(e, self.influx_init,
                     "Can not initialize Influxdb database")

    def influx_query_(self, q):
        """
        Runs an Influx db query
        """
        if self.influx_cli is None:
            self.err(
                self.influx_query_,
                "No database connected. Please initialize a connection")
            return
        try:
            return self.influx_cli.query(q)
        except Exception as e:
            self.err(e, self.influx_query_,
                     "Can not query database")

    def influx_count_(self, measurement):
        """
        Count the number of rows for a measurement
        """
        try:
            q = "select count(*) from " + measurement
            self.start("Querying: count ...")
            datalen = self.influx_cli.query(q)
            self.end("Finished querying")
            numrows = int(datalen[measurement][datalen[measurement].keys()[0]])
            return numrows
        except Exception as e:
            self.err(e, self.influx_count_,
                     "Can not count rows for measurement")

    def influx_to_csv(self, measurement, batch_size=5000):
        """
        Batch export data from an Influxdb measurement to csv
        """
        if self.autoprint is True:
            print("Processing data from InfluxDb to csv")
        try:
            q = "select count(*) from " + measurement
            numrows = self.influx_cli.query(q)[measurement].iloc[0, 0]
            self.info("Processing", str(numrows),
                      "datapoints from InfluxDb to csv")
            done = 0
            offset = 1
            while (done + 1) < numrows:
                q = "select * from " + measurement + \
                    " limit " + str(batch_size)
                if done > 0:
                    q += " offset " + str(offset)
                if self.autoprint is True:
                    self.start(
                        "Querying database for the next " +
                        str(batch_size) + " datapoints")
                res = self.influx_cli.query(q)
                if self.autoprint is True:
                    self.end("Finished to query")
                numres = 0
                try:
                    numres = len(res[measurement])
                except KeyError:
                    return
                df = res[measurement]
                ds2 = self.clone_(df)
                ds2.to_csv("data/" + measurement +
                           ".csv", index=False, mode='a')
                ds2.df = None
                if numres < batch_size:
                    done += numres
                else:
                    done += batch_size
                self.progress("Processed points", offset, "to", done)
                offset += batch_size
                # if (done + 1) == numrows:
                #    break
        except Exception as e:
            self.err(e, self.influx_to_csv,
                     "Can not transfer data from Influxdb to csv")
            return
        if self.autoprint is True:
            print("Finished processing data from InfluxDb to csv")

import warnings
import biman
import flydanaair
from exceptions import *

warnings.filterwarnings("ignore")

if __name__ == '__main__':

    site = ""
    while site != 'exit':
        print "Input desire site (f - flydanaair, b - biman) or print exit to quit:"
        site = raw_input()

        if site != "f" and site != "b":
            continue

        dep_city = raw_input("Depature city:")
        dest_city = raw_input("Destination city:")
        dep_date = raw_input("Depature date (DD/MM/YYYY):")
        ret_date = raw_input("Return date (if needed):")

        if not ret_date:
            ret_date = None
        try:
            if site == "f":
                scr = flydanaair.Flydanaair(dep_city, dest_city, dep_date, ret_date)
            else:
                scr = biman.Biman(dep_city, dest_city, dep_date, ret_date)
            print "Your results:\n"
            scr.make_request()
            scr.combine_flights()

        except ValueError:
            print "You input some incorrect information"
        except FlightsNotFound:
            print "There is no flights available for this date"
        except IncorrectAirport:
            print "You entered incorrect Departure or Destination city"

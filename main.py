import biman
import flydanaair
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':

    site = ""
    while site != 'exit':
        print "Input desire site (f - flydanaair, b - biman) or print exit to quit:"
        site = raw_input()

        if site != "f" and site != "b":
            continue

        f = raw_input("Depature city:")
        d = raw_input("Destination city:")
        df = raw_input("Depature date (DD/MM/YYYY):")
        dd = raw_input("Return date (if needed):")

        if not dd:
            dd = None
        try:
            print "Your results:\n"
            if site == "f":
                scr = flydanaair.Flydanaair('secure.flydanaair.com', f, d, df, dd)
            else:
                scr = biman.Biman('www.biman-airlines.com', f, d, df, dd)
            scr.make_request()
            scr.combine_flights()

        except ValueError:
            print "You input some incorrect information"
        except NotImplementedError:
            print "There is no flights available"

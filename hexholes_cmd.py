from argparse import ArgumentParser
import hexholegrid as hex

if __name__ == "__main__":
    option_parser = ArgumentParser(description="Probability arguments.")
    option_parser.add_argument("-iter", type=int, help="Number of iterations to run.",nargs=1, required=True)
    option_parser.add_argument("-gridsize", type=int, help="Size of the grid.", nargs=1, required=True)
    option_parser.add_argument("-p1", type=float,help="Probability 1 as positive float less than or equal to 1.0",nargs=1,required=True)
    option_parser.add_argument("-p2", type=float, help="Probability 2 as positive float less than or equal to 1.0",nargs=1,required=True)
    option_parser.add_argument("-p3", type=float, help="Probability 3 as positive float less than or equal to 1.0",nargs=1,required=True)
    option_parser.add_argument("-full_p", type=float, help="Probability of full cell turning OnlyA/B, as positive float less than or equal to 1.0",nargs=1,required=True)
    option_parser.add_argument("-only_p", type=float, help="Probability of OnlyA/B cell turning full, as positive float less than or equal to 1.0",nargs=1,required=True)
    args = option_parser.parse_args()
    grid = hex.HexholeGrid(None,args.p1[0],args.p2[0],args.p3[0],args.full_p[0],args.only_p[0],args.gridsize[0])
    grid.perform_iterations(args.iter[0])



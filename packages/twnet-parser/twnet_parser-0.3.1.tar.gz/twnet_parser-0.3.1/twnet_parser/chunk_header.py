from twnet_parser.pretty_print import PrettyPrint

class ChunkFlags(PrettyPrint):
    def __init__(self):
        self.resend = False
        self.vital = False
    def __repr__(self):
        return "<class: '" + str(self.__class__.__name__) + "'>: " + str(self.__dict__)

# same fields for 0.6 and 0.7
# different bit layout tho
class ChunkHeader(PrettyPrint):
    def __init__(self) -> None:
        self.flags: ChunkFlags = ChunkFlags()
        self.size: int = 0
        # TODO: should seq be a optional?
        #       so it can be None for non vital packages
        #       this could turn downstream users logic errors into
        #       crashes which would be easier to detect
        #
        #       Or is None annoying because it crashes
        #       and pollutes the code with error checking?
        #       Also the teeworlds code uses -1
        #       doing the same for someone who knows the codebase
        #       could also be nice
        self.seq: int = -1


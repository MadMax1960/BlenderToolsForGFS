from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format
from .Materials.Binary import MaterialPayload
from .Model.Binary import ModelPayload
from .Textures.Binary import TexturePayload
from .Animations.Binary import AnimationPayload
from .Physics.Binary import PhysicsPayload
from .CommonStructures import Blob


class HasAnimationsError(Exception):
    pass

class UnsupportedVersionError(Exception):
    pass

class GFS0ContainerBinary(Serializable):
    SIZE = 0x0C
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.version = None
        self.type = None
        self.size = None
        self.padding_0x0C = 0
        self.count = None
        self.data = []
        
    def __repr__(self):
        return f"[GFS::Container] {safe_format(self.version, hex32_format)} {safe_format(self.type, hex32_format)} {self.size}"


    def read_write(self, rw):
        self.version      = rw.rw_uint32(self.version)
        self.type         = rw.rw_uint32(self.type)
        self.size         = rw.rw_uint32(self.size)
        
        # Need to be extremely careful here...
        # print(f"VERSION: {self.version:0>8x}, TYPE: {hex(self.type)}, SIZE: {self.size}")
        # if self.version < 0x01104030 and (rw.mode() == "read" or rw.mode() == "write"):
        #     raise UnsupportedVersionError(f"GFS file version '{safe_format(self.version, hex32_format)}' is not currently supported")

        args = []
        if self.type == 0x00000000:
            pass
        elif self.type == 0x00000001:
            pass
        elif self.type == 0x00010003: # Model
            dtype = ModelPayload
        elif self.type == 0x000100F8: # Unknown
            dtype = Blob
        elif self.type == 0x000100F9: # Physics
            dtype = PhysicsPayload
        elif self.type == 0x000100FB: # Materials
            dtype = MaterialPayload
        elif self.type == 0x000100FC: # Textures
            dtype = TexturePayload
        elif self.type == 0x000100FD: # Animations
            dtype = AnimationPayload
        else:
            raise NotImplementedError(f"Unrecognised GFS Container Type: '{safe_format(self.type, hex32_format)}'")
            

        if self.type == 0x00000001:
            return
        elif self.type in [0x000100F8]: # Can be removed later
            args = [self.size - 0x10]
        
        self.padding_0x0C = rw.rw_uint32(self.padding_0x0C)
        rw.assert_equal(self.padding_0x0C, 0) 
        
        if self.type == 0x00000000:
            return
        
        if rw.mode() == "read":
            self.data = dtype()
        assert type(self.data) == type(dtype()), f"{type(self.data)}, {type(dtype())}"
        rw.rw_obj(self.data, self.version, *args) # Can remove *args when Blob can be removed

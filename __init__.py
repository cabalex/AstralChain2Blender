bl_info = {
    "name": "AstralChain2Blender (Astral Chain Model Importer)",
    "author": "Cabalex and Woeful_Wolf (Original by C4nf3ng)",
    "version": (2, 2),
    "blender": (2, 80, 0),
    "api": 38019,
    "location": "File > Import",
    "description": "Import Astral Chain Model Data",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}

import bpy
import os
from bpy_extras.io_utils import ExportHelper,ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty

class ImportAstralChain(bpy.types.Operator, ImportHelper):
    '''Load an Astral Chain WMB File.'''
    bl_idname = "import_scene.wmb_data_ac"
    bl_label = "Import WMB Data"
    bl_options = {'PRESET'}
    filename_ext = ".wmb"
    filter_glob: StringProperty(default="*.wmb", options={'HIDDEN'})

    reset_blend: bpy.props.BoolProperty(name="Reset Blender Scene on Import", default=True)

    def execute(self, context):
        from . import wmb_importer
        if self.reset_blend:
            wmb_importer.reset_blend()
        return wmb_importer.main(False, self.filepath)

class ImportDATAstralChain(bpy.types.Operator, ImportHelper):
    '''Load an Astral Chain DTT (and DAT) File.'''
    bl_idname = "import_scene.dtt_data_ac"
    bl_label = "Import DTT (and DAT) Data"
    bl_options = {'PRESET'}
    filename_ext = ".dtt"
    filter_glob: StringProperty(default="*.dtt", options={'HIDDEN'})

    reset_blend: bpy.props.BoolProperty(name="Reset Blender Scene on Import", default=True)
    bulk_import: bpy.props.BoolProperty(name="Bulk Import All DTT/DATs In Folder (Experimental)", default=False)

    def execute(self, context):
        from . import wmb_importer
        if self.reset_blend:
            wmb_importer.reset_blend()
        if self.bulk_import:
            folder = os.path.split(self.filepath)[0]
            for filename in os.listdir(folder):
                if filename[-4:] == '.dtt':
                    try:
                        filepath = folder + '\\' + filename
                        head = os.path.split(filepath)[0]
                        tail = os.path.split(filepath)[1]
                        tailless_tail = tail[:-4]
                        dat_filepath = head + '\\' + tailless_tail + '.dat'
                        extract_dir = head + '\\astralchain2blender_extracted'
                        from . import dat_unpacker
                        if os.path.isfile(dat_filepath):
                            dat_unpacker.main(dat_filepath, extract_dir + '\\' + tailless_tail + '.dat', dat_filepath)   # dat
                        else:
                            print('DAT not found. Only extracting DTT. (No materials will automatically be imported)')

                        wtp_filename = dat_unpacker.main(filepath, extract_dir + '\\' + tailless_tail + '.dtt', filepath)       # dtt

                        wmb_filepath = extract_dir + '\\' + tailless_tail + '.dtt\\' + wtp_filename[:-4] + '.wmb'
                        if not os.path.exists(wmb_filepath):
                            wmb_filepath = extract_dir + '\\' + tailless_tail + '.dat\\' + wtp_filename[:-4] + '.wmb'                     # if not in dtt, then must be in dat

                        wmb_importer.main(wmb_filepath)
                    except:
                        print('ERROR: FAILED TO IMPORT', filename)
            return {'FINISHED'}

        else:
            head = os.path.split(self.filepath)[0]
            tail = os.path.split(self.filepath)[1]
            tailless_tail = tail[:-4]
            dat_filepath = head + '\\' + tailless_tail + '.dat'
            extract_dir = head + '\\astralchain2blender_extracted'
            from . import dat_unpacker
            if os.path.isfile(dat_filepath):
                dat_unpacker.main(dat_filepath, extract_dir + '\\' + tailless_tail + '.dat', dat_filepath)   # dat
            else:
                print('DAT not found. Only extracting DTT. (No materials will automatically be imported)')

            wtp_filename = dat_unpacker.main(self.filepath, extract_dir + '\\' + tailless_tail + '.dtt', self.filepath)       # dtt

            wmb_filepath = extract_dir + '\\' + tailless_tail + '.dtt\\' + wtp_filename[:-4] + '.wmb'
            if not os.path.exists(wmb_filepath):
                wmb_filepath = extract_dir + '\\' + tailless_tail + '.dat\\' + wtp_filename[:-4] + '.wmb'                     # if not in dtt, then must be in dat

            from . import wmb_importer
            return wmb_importer.main(wmb_filepath)

# Registration

def ac_menu_func_import(self, context):
    self.layout.operator(ImportAstralChain.bl_idname, text="WMB File for Astral Chain (.wmb)")

def ac_menu_func_import_dat(self, context):
    self.layout.operator(ImportDATAstralChain.bl_idname, text="DTT File for Astral Chain (.dtt)")

def register():
    bpy.utils.register_class(ImportAstralChain)
    bpy.utils.register_class(ImportDATAstralChain)
    bpy.types.TOPBAR_MT_file_import.append(ac_menu_func_import)
    bpy.types.TOPBAR_MT_file_import.append(ac_menu_func_import_dat)

def unregister():
    bpy.utils.unregister_class(ImportAstralChain)
    bpy.utils.unregister_class(ImportDATAstralChain)
    bpy.types.TOPBAR_MT_file_import.remove(ac_menu_func_import)
    bpy.types.TOPBAR_MT_file_import.remove(ac_menu_func_import_dat)


if __name__ == '__main__':
    register()

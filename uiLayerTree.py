import bpy
from vtools_multiLayerPainting import paintingLayers

#-- DEF CALLBACKS ---#


def cb_selectLayerSet(self, value):
    
    
    bpy.context.scene.mlpLayerTreeCollection.clear()
    bpy.context.scene.mlpLayerTreeCollection_ID = -1
    
    bpy.ops.vtoolpt.collectsetlayers()
    

def deselectAllLayerNodes():
    
    for i in range(0, len(bpy.context.scene.mlpLayerTreeCollection)):
        lNode = paintingLayers.getLayerNodeById(i)
        if lNode != None:
            if lNode.node_tree != None:
                colorNode = lNode.node_tree.nodes["MT_TexColor"]
                maskNode = lNode.node_tree.nodes["MT_TexMask"]
                
                lNode.node_tree.nodes.active = lNode.node_tree.nodes[0]
                colorNode.select = False
                maskNode.select = False
                lNode.select = False
    
    
def findPaintingSlot(pImageName):
    
    idImage = bpy.context.object.active_material.texture_paint_images.find(pImageName)
    if idImage != -1:
        bpy.context.object.active_material.paint_active_slot = idImage
                  
    
def cb_selectPaintingLayer(self,value):
    
    
    lNode = paintingLayers.getLayerNodeById(bpy.context.scene.mlpLayerTreeCollection_ID)
    
    if lNode != None:
        
        deselectAllLayerNodes()
        nodeSet = paintingLayers.getActiveLayerSet(False)
        mainTree = nodeSet.node_tree
        
        #selecciona y activa los nodos activos 
        
        nodeSet.select = True
        bpy.context.object.active_material.node_tree.nodes.active = nodeSet
        lNode.select = True
        mainTree.nodes.active = lNode
        
        #elige la textura a pintar
        
        cs = paintingLayers.getLayerColorSpace()
        if cs == "color":
            colorNode = lNode.node_tree.nodes["MT_TexColor"]
            colorNode.select = True
            lNode.node_tree.nodes.active = colorNode
            
            colorImage = colorNode.image
            
            
            if colorImage != None:
                findPaintingSlot(colorImage.name)
                bpy.context.tool_settings.image_paint.canvas = bpy.data.images[colorImage.name]
                #colorImage.alpha_mode = "STRAIGHT" #"PREMUL" #IMAGE ALPHA MODE AS PREMULTIPLIED
            else:
                bpy.context.tool_settings.image_paint.canvas = None
                 
        else:
            maskNode = lNode.node_tree.nodes["MT_TexMask"]
            maskNode.select = True
            lNode.node_tree.nodes.active = maskNode
            
            maskImage = maskNode.image
            if maskImage != None:
                findPaintingSlot(maskImage.name)
                bpy.context.tool_settings.image_paint.canvas = bpy.data.images[maskImage.name]
                #maskImage.alpha_mode = "STRAIGHT" #"PREMUL" #IMAGE ALPHA MODE AS PREMULTIPLIED
            else:
                bpy.context.tool_settings.image_paint.canvas = None
        
        """
        if lNode.node_tree.nodes["MT_TexMask"].image != None:
            lNode.node_tree.nodes["PL_InputMaskOpacity"].outputs[0].default_value = 1
        else:
            lNode.node_tree.nodes["PL_InputMaskOpacity"].outputs[0].default_value = 0
        """
    else:
        deselectAllLayerNodes()
        #bpy.context.object.active_material.paint_active_slot = -1
        
    bpy.context.scene.mlpFilterLayerCollection.clear()
    bpy.context.scene.mlpFilterLayerCollection_ID = -1
    
    bpy.ops.vtoolpt.collectlayerfilter()
    
                

def cb_setLayerVisibilty(self, value):
    
    #lNode = paintingLayers.getLayerNodeById(bpy.context.scene.mlpLayerTreeCollection_ID)
    lNode = paintingLayers.getLayerNodeById(self.layerID)
    
    if self.visible == True:
        #lNode.node_tree.nodes["PL_OpacityOffset"].inputs[0].default_value =  1
        lNode.inputs["Enabled"].default_value = 1
    else:
        #lNode.node_tree.nodes["PL_OpacityOffset"].inputs[0].default_value =  0
        lNode.inputs["Enabled"].default_value = 0
    
def cb_renameLayerSet(self, value):
    
    lsNode = paintingLayers.getActiveLayerSetByName(self.layerSetName)
    if lsNode != None:
        lsNode.label = self.name


def cb_renamePaintingLayer(self, value):

    lNode = paintingLayers.getLayerNodeByName(self.layerName)
    if lNode != None:
        lNode.label = self.name

def cb_selectFilterLayer(self, value):
    
    return None

    
# --- FILTERS TREE ---------#

class VTOOLS_UL_FilterlayerTree(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
            layout.prop(item, "name", text="", emboss=False, translate=False)
         
class VTOOLS_CC_FilterlayerCollection(bpy.types.PropertyGroup):
       
    name : bpy.props.StringProperty(default='')
    filterLayerID : bpy.props.IntProperty()
    filterLayerName : bpy.props.StringProperty(name="filterLayer", default="filterLayer")
        
# --- PAINTING LAYER TREE --- #

class VTOOLS_UL_layerTree(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
        image = None
        selectedLayer = paintingLayers.getLayerNodeSelected()
        if selectedLayer != None:
            itemLayerNode = paintingLayers.getLayerNodeById(item.layerID)
            layerNode = paintingLayers.getLayerNodeByName(item.layerName)
            isSelectedLayer = selectedLayer.name == item.layerName
            cs = item.colorSpace
            
            colorEmboss = False
            maskEmboss = False
            

            if isSelectedLayer:
                if cs == "color":
                    layout.label(text="", icon="IMAGE")
                    colorEmboss = True
                else:
                    layout.label(text="", icon="IMAGE_ALPHA") 
                    maskEmboss = True
            else:
                layout.label(text="", icon="DOT") 
                
   
            row = layout.row(align=True)
            
            
            #row.operator(paintingLayers.VTOOLS_OP_DuplicatePaintingLayer.bl_idname, text="", icon='HIDE_OFF')
            
            if layerNode.node_tree != None:
                imageColor = layerNode.node_tree.nodes["MT_TexColor"].image
                imageMask = layerNode.node_tree.nodes["MT_TexMask"].image
                
                """
                if imageMask.name == "MT_baseTexMask":
                    imageMask = None
                """    
                
                if imageColor != None:
                    
                    icon = None
                    if imageColor.preview != None:
                        icon = imageColor.preview.icon_id
                    else:
                        icon = imageColor.preview_ensure().icon_id
                            
                    opm = row.operator(paintingLayers.VTOOLS_OP_SelectLayerColorSpace.bl_idname, text="", icon_value=icon, emboss=colorEmboss)   
                    opm.color = "color"
                    opm.layerID = item.layerID
                    #row.label(text="", icon_value=imageColor.preview.icon_id)
                else:
                    #row.label(text="", icon="FILE") 
                    opm = row.operator(paintingLayers.VTOOLS_OP_SelectLayerColorSpace.bl_idname, text="", icon="FILE", emboss=colorEmboss)   
                    opm.color = "color"
                    opm.layerID = item.layerID
                    
                if imageMask != None:
                    
                    icon = None
                    if imageMask.preview != None:
                        icon = imageMask.preview.icon_id
                    else:
                        icon = imageMask.preview_ensure().icon_id
                        
                    opm = row.operator(paintingLayers.VTOOLS_OP_SelectLayerColorSpace.bl_idname, text="", icon_value=icon, emboss=maskEmboss)   
                    opm.color = "mask"
                    opm.layerID = item.layerID
                    #row.label(text="", icon_value=imageMask.preview.icon_id)
                else:
                    #row.label(text="", icon="FILE") 
                    opm = row.operator(paintingLayers.VTOOLS_OP_SelectLayerColorSpace.bl_idname, text="", icon="FILE", emboss=maskEmboss)   
                    opm.color = "mask"
                    opm.layerID = item.layerID
 
                    
                row = layout.row(align=True)
                row.enabled = isSelectedLayer  
                
       
                if cs == "color":
                    row.prop(layerNode.node_tree.nodes["MT_TexColor"], "image", text="")
                else:
                    maskNode = layerNode.node_tree.nodes["MT_TexMask"]
                    row.prop(maskNode, "image", text="")

                row = layout.row(align=True)
                row.prop(item, "visible", text="", icon='HIDE_OFF', translate=False)           
        
class VTOOLS_CC_layerTreeCollection(bpy.types.PropertyGroup):
       
    name : bpy.props.StringProperty(default='', update = cb_renamePaintingLayer)
    layerID : bpy.props.IntProperty()
    layerName : bpy.props.StringProperty(name="layerName", default="layerName")
    
    colorSpace : bpy.props.EnumProperty(
    items=(
        ("color", "Color Texture", 'color space',  'IMAGE', 1),
        ("mask", "Mask Texture", 'mask space',  'IMAGE_ALPHA', 2),
    ),
    name="colorSpaceEnum",
    default="color",
    update = cb_selectPaintingLayer
    )
    visible : bpy.props.BoolProperty(default=True, update=cb_setLayerVisibilty)
    


# --- LAYER SET TREE ---------#

class VTOOLS_UL_layerSetTree(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "name", text="", emboss=False, translate=False)
        #layout.prop(item, "layerSetName", text="", emboss=False, translate=False)
        
            
class VTOOLS_CC_layerSetCollection(bpy.types.PropertyGroup):
       
    name : bpy.props.StringProperty(default='', update=cb_renameLayerSet)
    layerSetID : bpy.props.IntProperty()
    layerSetName : bpy.props.StringProperty(name="layerSetName", default="layerSetName")
    
# ----- REGISTER -------------#


def register():
    
    bpy.utils.register_class(VTOOLS_CC_layerTreeCollection)
    bpy.utils.register_class(VTOOLS_UL_layerTree)
    bpy.utils.register_class(VTOOLS_CC_layerSetCollection)
    bpy.utils.register_class(VTOOLS_UL_layerSetTree)
    bpy.utils.register_class(VTOOLS_UL_FilterlayerTree)
    bpy.utils.register_class(VTOOLS_CC_FilterlayerCollection)
    
    
    bpy.types.Scene.mlpLayerTreeCollection = bpy.props.CollectionProperty(type=VTOOLS_CC_layerTreeCollection)
    bpy.types.Scene.mlpLayerTreeCollection_ID = bpy.props.IntProperty(update=cb_selectPaintingLayer, default = -1)
    #bpy.types.Scene.mlpLayerTreeCollection_ID = bpy.props.IntProperty(default = -1)
    
    #bpy.context.scene.mlpLayerTreeCollection.clear()
    #bpy.context.scene.mlpLayerTreeCollection_ID = -1
    
    bpy.types.Scene.mlpLayerSetsCollection = bpy.props.CollectionProperty(type=VTOOLS_CC_layerSetCollection)
    bpy.types.Scene.mlpLayerSetsCollection_ID = bpy.props.IntProperty(update=cb_selectLayerSet, default = -1) #bpy.props.StringProperty(update = callback_editFilter)
    
    #bpy.context.scene.mlpLayerSetsCollection.clear()
    #bpy.context.scene.mlpLayerSetsCollection_ID = -1
    
    bpy.types.Scene.mlpFilterLayerCollection = bpy.props.CollectionProperty(type=VTOOLS_CC_FilterlayerCollection)
    bpy.types.Scene.mlpFilterLayerCollection_ID = bpy.props.IntProperty(update=cb_selectFilterLayer, default = -1) #bpy.props.StringProperty(update = callback_editFilter)
    
    #bpy.context.scene.mlpFilterLayerCollection.clear()
    #bpy.context.scene.mlpFilterLayerCollection_ID = -1
    
    bpy.types.Scene.mlpDefaultImageLayerSize = bpy.props.IntProperty(default = 1024)
    
    return {'FINISHED'}

def unregister():
    
    bpy.utils.unregister_class(VTOOLS_CC_layerTreeCollection)
    bpy.utils.unregister_class(VTOOLS_UL_layerTree)
    bpy.utils.unregister_class(VTOOLS_CC_layerSetCollection)
    bpy.utils.unregister_class(VTOOLS_UL_layerSetTree)
    bpy.utils.unregister_class(VTOOLS_UL_FilterlayerTree)
    bpy.utils.unregister_class(VTOOLS_CC_FilterlayerCollection)
    
    del bpy.types.Scene.mlpLayerTreeCollection_ID
    del bpy.types.Scene.mlpLayerTreeCollection
    
    del bpy.types.Scene.mlpLayerSetsCollection_ID
    del bpy.types.Scene.mlpLayerSetsCollection
    
    del bpy.types.Scene.mlpFilterLayerCollection_ID
    del bpy.types.Scene.mlpFilterLayerCollection
    
    del bpy.types.Scene.mlpDefaultImageLayerSize
     
    return {'FINISHED'}

classes = (
    
    VTOOLS_CC_layerTreeCollection,
    VTOOLS_UL_layerTree,

)


# ---------------------------------- #






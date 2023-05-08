import bpy


def create_PLOpacityGroup():
    
    opGroup = bpy.data.node_groups.new('MTPaintLayerOpacityGroup', 'ShaderNodeTree')
    
    #INPUTS
    opInputs = opGroup.nodes.new('NodeGroupInput')
    opInputs.name = "MT_OpacitySystemInputs"
    opInputs.label = "Opacity System Inputs"
    
    
    inputColor = opGroup.inputs.new('NodeSocketColor','Color')
    inputColor.default_value = [0,0,0,0]
    
    inputOpacity = opGroup.inputs.new('NodeSocketFloat','Opacity')
    inputEnabled = opGroup.inputs.new('NodeSocketFloat','Enabled')
     
    
    #OUTPUTS
    opOutputs = opGroup.nodes.new('NodeGroupOutput')
    opOutputs.name = "MT_OpacitySystemOutputs"
    opOutputs.label = 'Opacity System Opacity'
    
    outputColor = opGroup.outputs.new('NodeSocketColor','Color')
    outputColor.default_value = [0,0,0,0]
    
    #MAT SYSTEM
    n_opacityControl = opGroup.nodes.new('ShaderNodeMath')
    n_opacityControl.operation = "MULTIPLY"
    n_opacityControl.use_clamp = True
    
    #MAT SYSTEM
    n_layerEnable = opGroup.nodes.new('ShaderNodeMath')
    n_layerEnable.operation = "MULTIPLY"
    n_layerEnable.use_clamp = True
    
    
    #LINKS
    opGroup.links.new(opInputs.outputs[inputColor.name], n_opacityControl.inputs[0]) 
    opGroup.links.new(opInputs.outputs[inputOpacity.name], n_opacityControl.inputs[1])
    
    opGroup.links.new(n_opacityControl.outputs["Value"], n_layerEnable.inputs[0])
    opGroup.links.new(opInputs.outputs[inputEnabled.name], n_layerEnable.inputs[1])
    
    opGroup.links.new(n_layerEnable.outputs["Value"], opOutputs.inputs[outputColor.name])
    
    return opGroup
    
def create_PLInputs(pGroupNode):
    
    mt_node = pGroupNode
    
    #INPUT FRAME
    n_inputFrame = mt_node.nodes.new('NodeFrame')
    n_inputFrame.name = "MT_FrameInputs"
    n_inputFrame.label = "Frame Inputs"
    
    #GROUP INPUTS
    mt_nodeInputs = mt_node.nodes.new('NodeGroupInput')
    mt_nodeInputs.name = "MT_LayerInput"
    mt_nodeInputs.label = "Painting Layer Inputs"
    
    mt_nodeInputs.parent = n_inputFrame
    
    #INPUT OPACITY
    inputLayerOpacity = mt_node.inputs.new('NodeSocketFloat','Opacity')
    inputLayerOpacity.min_value = 0
    inputLayerOpacity.max_value = 1
    inputLayerOpacity.default_value = 1
    
    #INPUT GLOBAL FILTER
    inputGlobalFilter = mt_node.inputs.new('NodeSocketFloat','Global Filter')
    inputGlobalFilter.min_value = 0
    inputGlobalFilter.max_value = 1
    inputGlobalFilter.default_value = 0
    
    #INPUT LAYER ENABLED
    inputLayerEnabled = mt_node.inputs.new('NodeSocketInt','Enabled')
    inputLayerEnabled.min_value = 0
    inputLayerEnabled.max_value = 1
    inputLayerEnabled.default_value = 1
    
    #INPUT COLOR BELOW
    inputColorBelow = mt_node.inputs.new('NodeSocketColor','Color Below')
    inputColorBelow.default_value = [0,0,0,0]
    
    inputColorAlpha = mt_node.inputs.new('NodeSocketColor','Alpha Below')
    inputColorAlpha.default_value = [0,0,0,0]
    
    #POSITIONS
    n_inputFrame.location = (-500,0)
    
    return [inputLayerOpacity, inputGlobalFilter, inputLayerEnabled, inputColorBelow, inputColorAlpha]

def create_PLTextures(pGroupNode):
    
    mt_node = pGroupNode
     
    #LAYOUT FRAME
    mt_texturesFrame = mt_node.nodes.new('NodeFrame')
    mt_texturesFrame.name = "MT_textures"
    mt_texturesFrame.label = "Textures"
    
    #COLOR TEXTURE
    colorTexture = mt_node.nodes.new("ShaderNodeTexImage")
    colorTexture.label = "COLOR"
    colorTexture.name = "MT_TexColor"
    #colorTexture.alpha_mode = "PREMUL"
    
    """
    #BASE ALPHA TEXTURE - NEEDED IN CYCLES IF NOT PRRSENT NONE ALPHA = PURPLE
    
    if bpy.data.images.find("MT_baseTexMask") == -1:
        baseMaskImage = bpy.data.images.new(name="MT_baseTexMask", width=1, height=1, alpha=False)
        pixels = baseMaskImage.pixels
        numPixels = len(pixels)
        for i in range(0, numPixels, 4):
            for j in range(4):
                pixels[j] = 1.0
    

    baseMaskImage = bpy.data.images["MT_baseTexMask"]
    baseMaskImage.use_fake_user = True
    """
    
    #ALPHA TEXTURE
    maskTexture = mt_node.nodes.new("ShaderNodeTexImage")
    maskTexture.label = "ALPHA"
    maskTexture.name = "MT_TexMask"    
    #maskTexture.image = bpy.data.images["MT_baseTexMask"]

    
    #UV NODES
    colorUVNode = mt_node.nodes.new("ShaderNodeUVMap")
    maskUVNode = mt_node.nodes.new("ShaderNodeUVMap")
    colorUVNode.name = "colorUVNode"
    maskUVNode.name = "maskUVNode"
    
    #MAPPING NODES
    colorMapNode = mt_node.nodes.new("ShaderNodeMapping")
    colorMapNode.name = "colorMapNode"
    
    maskMapNode = mt_node.nodes.new("ShaderNodeMapping")
    maskMapNode.name = "maskMapNode"
   
    
    #LAYOUT FRAME PARENTING
    colorTexture.parent = mt_texturesFrame
    maskTexture.parent = mt_texturesFrame
    colorUVNode.parent = mt_texturesFrame
    maskUVNode.parent = mt_texturesFrame
    colorMapNode.parent = mt_texturesFrame
    maskMapNode.parent = mt_texturesFrame
    
    #NODE LOCATION
    colorMapNode.location = (0,-230)
    colorUVNode.location = (0,-630)
    maskTexture.location = (600,0)
    maskMapNode.location = (600,-230)
    maskUVNode.location = (600,-630)
    mt_texturesFrame.location = (-400,-750)
    
    
    #LINKS COLOR
    mt_node.links.new(colorUVNode.outputs["UV"], colorMapNode.inputs["Vector"]) #UV TO MAPPING
    mt_node.links.new(colorMapNode.outputs["Vector"], colorTexture.inputs["Vector"]) #MAPPING TO TEXTURE
    
    #LINKS ALPHA
    mt_node.links.new(maskUVNode.outputs["UV"], maskMapNode.inputs["Vector"]) #UV TO MAPPING
    mt_node.links.new(maskMapNode.outputs["Vector"], maskTexture.inputs["Vector"]) #MAPPING TO TEXTURE
    

    return [colorTexture, maskTexture]


def create_PLOpacityControls(pMainGroup, pOpacityGroup):
    
    coreGroup = pMainGroup #bpy.data.node_groups.new('MTPaintLayerCore', 'ShaderNodeTree')
    links = coreGroup.links
    
    #INPUTS
    coreInputs = coreGroup.nodes["MT_LayerInput"] # coreGroup.nodes.new('NodeGroupInput')
    
    inputTexColor = coreGroup.nodes["MT_TexColor"].outputs["Color"]
    inputTexAlpha = coreGroup.nodes["MT_TexColor"].outputs["Alpha"]
    
    inputMaskColor = coreGroup.nodes["MT_TexMask"].outputs["Color"]
    inputMaskAlpha = coreGroup.nodes["MT_TexMask"].outputs["Alpha"]
    
    inputLayerOpacity = coreGroup.nodes["MT_layerOpacity"].outputs["Value"]
    # ---- NODES ----------- #
    
    #OUTPUT FRAME
    n_maskConversion = coreGroup.nodes.new('NodeFrame')
    n_maskConversion.name = "MT_FrameMaskConvert"
    n_maskConversion.label = "Frame Mask Convert"
    
    #COLOR OPACITY CONTROL
    n_opacityColor = coreGroup.nodes.new('ShaderNodeGroup')
    n_opacityColor.node_tree = bpy.data.node_groups[pOpacityGroup]   
    n_opacityColor.name = "MT_ColorLayerOpacity"
    n_opacityColor.label = "Color Layer Opacity"
    
    #ALPHA OPACITY CONTROL
    n_opacityAlpha = coreGroup.nodes.new('ShaderNodeGroup')
    n_opacityAlpha.node_tree = bpy.data.node_groups[pOpacityGroup]   
    n_opacityAlpha.name = "MT_AlphaLayerOpacity"
    n_opacityAlpha.label = "Alpha Layer Opacity"
    
    # ---------------------- MASK CONVERSION  ------------------- #
    
    #MISSING TEXTURE 
    n_missingTexture = coreGroup.nodes.new("ShaderNodeRGB")
    n_missingTexture.name = "MT_MissingTextureColor"
    n_missingTexture.label = "Missing Texture Color"
    n_missingTexture.outputs[0].default_value = (1,0,1,1)
    
    n_missingTexture.parent = n_maskConversion
    
    #DIVIDE MISSING
    n_divideColorMissing = coreGroup.nodes.new("ShaderNodeMath")
    n_divideColorMissing.name = "MT_divideColorMissing"
    n_divideColorMissing.label = "Divide Color Missing"
    n_divideColorMissing.operation = "DIVIDE"
    n_divideColorMissing.use_clamp = True
    n_divideColorMissing.inputs[0].default_value = 0
    n_divideColorMissing.inputs[1].default_value = 0
    
    n_divideColorMissing.parent = n_maskConversion
    
    n_divideAlphaMissing = coreGroup.nodes.new("ShaderNodeMath")
    n_divideAlphaMissing.name = "MT_divideAlphaMissing"
    n_divideAlphaMissing.label = "Divide Alpha Missing"
    n_divideAlphaMissing.operation = "DIVIDE"
    n_divideAlphaMissing.use_clamp = True
    n_divideAlphaMissing.inputs[0].default_value = 0
    n_divideAlphaMissing.inputs[1].default_value = 0
    
    n_divideAlphaMissing.parent = n_maskConversion
    
    #COMPARE MISSING
    n_compareColorMissing = coreGroup.nodes.new("ShaderNodeMix")
    n_compareColorMissing.name = "MT_compareColorMissing"
    n_compareColorMissing.label = "Compare Color Missing"
    n_compareColorMissing.blend_type = "MIX"
    n_compareColorMissing.data_type = "RGBA"  
    n_compareColorMissing.inputs[0].default_value = 1
    n_compareColorMissing.clamp_result = True
    n_compareColorMissing.inputs[7].default_value = (1,1,1,1)
    
    n_compareColorMissing.parent = n_maskConversion
    
    n_compareAlphaMissing = coreGroup.nodes.new("ShaderNodeMix")
    n_compareAlphaMissing.name = "MT_compareAlphaMissing"
    n_compareAlphaMissing.label = "Compare Alpha Missing"
    n_compareAlphaMissing.blend_type = "MIX"
    n_compareAlphaMissing.data_type = "RGBA"  
    n_compareAlphaMissing.inputs[0].default_value = 1
    n_compareAlphaMissing.clamp_result = True
    n_compareAlphaMissing.inputs[7].default_value = (1,1,1,1)
    
    n_compareAlphaMissing.parent = n_maskConversion
    
    #CONVERT BW
    n_convertBW = coreGroup.nodes.new("ShaderNodeRGBToBW")
    n_convertBW.name = "MT_ConverToBW"
    n_convertBW.label = "Conver to BW"
    
    n_convertBW.parent = n_maskConversion
    
    #MIX COLOR
    n_mixAlphas = coreGroup.nodes.new("ShaderNodeMix")
    n_mixAlphas.name = "MT_MixColorAndMaskAlphas"
    n_mixAlphas.label = "Mix Color/Mask"
    n_mixAlphas.blend_type = "MULTIPLY"
    n_mixAlphas.data_type = "RGBA"  
    n_mixAlphas.inputs[0].default_value = 1
    n_mixAlphas.clamp_result = True
    
    n_mixAlphas.parent = n_maskConversion
    
    #GREATHER THAN
    n_alphaGreaterThan = coreGroup.nodes.new("ShaderNodeMath")
    n_alphaGreaterThan.name = "MT_alphaGreaterThan"
    n_alphaGreaterThan.label = "Alpha Greater Than"
    n_alphaGreaterThan.operation = "GREATER_THAN"
    n_alphaGreaterThan.use_clamp = True
    n_alphaGreaterThan.inputs[0].default_value = 0.0
    n_alphaGreaterThan.inputs[1].default_value = 0
    
    n_alphaGreaterThan.parent = n_maskConversion

    # ----------- LINKS ------------------ #
    
    #MISSING TEXTURE LINKS
    links.new(n_missingTexture.outputs["Color"], n_divideColorMissing.inputs[1])
    links.new(n_missingTexture.outputs["Color"], n_divideAlphaMissing.inputs[1])
    
    links.new(inputMaskColor, n_divideColorMissing.inputs[0]) 
    links.new(inputMaskAlpha, n_divideAlphaMissing.inputs[0])
     
    links.new(inputMaskColor, n_compareColorMissing.inputs[6]) 
    links.new(inputMaskAlpha, n_compareAlphaMissing.inputs[6])
    
    links.new(n_divideColorMissing.outputs["Value"], n_compareColorMissing.inputs["Factor"]) 
    links.new(n_divideAlphaMissing.outputs["Value"], n_compareAlphaMissing.inputs["Factor"])
    
    #OPACITY CONTROL LINKS
    links.new(inputLayerOpacity, n_opacityColor.inputs["Opacity"]) #OPACITY TO ALPHA COLOR
    links.new(inputLayerOpacity, n_opacityAlpha.inputs["Opacity"]) #OPACTIY TO ALPHA MASK
    
    #TEXTURE LINKS 
    links.new(inputTexAlpha, n_opacityColor.inputs["Color"]) #TEX ALPHA TO ALPHA COLOR
    links.new(inputTexAlpha, n_mixAlphas.inputs[6]) #TEX ALPHA TO MIX
    links.new(n_compareAlphaMissing.outputs[2], n_alphaGreaterThan.inputs[0]) #TEX ALPHA TO MIX
    
    #MASK CONVERSION LINKS
    links.new(n_compareColorMissing.outputs[2], n_convertBW.inputs["Color"]) #MASK COLOR TO BW
    links.new(n_convertBW.outputs["Val"], n_mixAlphas.inputs[7]) #MASK COLOR TO BW
    links.new(n_mixAlphas.outputs[2], n_opacityAlpha.inputs["Color"]) #BW / MIX TO OPACITY
    links.new(n_alphaGreaterThan.outputs["Value"], n_mixAlphas.inputs["Factor"]) #BW / MIX TO OPACITY
    
    #POSITION
    n_maskConversion.location = (600, -750)
    #n_missingTexture.location = (,)
    n_divideColorMissing.location = (200,0)
    n_divideAlphaMissing.location = (200,-200)
    n_compareColorMissing.location = (400,0)
    n_compareAlphaMissing.location = (400,-300)
    n_convertBW.location = (600,0)
    n_mixAlphas.location = (800,0)
    n_alphaGreaterThan.location = (600,-150)
    
    return coreGroup

def create_PLGlobalFilterOpacity(pMainGroup):
        
    globalFilterOpacity = pMainGroup
    
    mainInputs = globalFilterOpacity.nodes["MT_LayerInput"]
    inputGlobalFilter = mainInputs.outputs["Global Filter"]
    inputLayerOpacity = mainInputs.outputs["Opacity"]
    inputLayerEnabled = mainInputs.outputs["Enabled"]
    
    #MATH OPACITY GLOBAL
    n_opacityGlobalFilter = globalFilterOpacity.nodes.new('ShaderNodeMath')
    n_opacityGlobalFilter.operation = "MULTIPLY"
    n_opacityGlobalFilter.name = "MT_OpacityGlobalFiler"
    n_opacityGlobalFilter.label = "Opacity Global Filter"
    
    #MATH OPACITY ENABLE
    n_layerEnable = globalFilterOpacity.nodes.new('ShaderNodeMath')
    n_layerEnable.operation = "MULTIPLY"
    n_layerEnable.name = "MT_layerOpacity"
    n_layerEnable.label = "Layer Opacity"
        
    #LINKS
    globalFilterOpacity.links.new(inputLayerOpacity, n_layerEnable.inputs[0])
    globalFilterOpacity.links.new(inputLayerEnabled, n_layerEnable.inputs[1])
    
    globalFilterOpacity.links.new(n_layerEnable.outputs[0], n_opacityGlobalFilter.inputs[0])
    globalFilterOpacity.links.new(inputGlobalFilter, n_opacityGlobalFilter.inputs[1])
    
    #PARENT AND POSITION
    n_opacityGlobalFilter.parent = globalFilterOpacity.nodes["MT_FrameInputs"]
    n_layerEnable.parent = globalFilterOpacity.nodes["MT_FrameInputs"]
    n_opacityGlobalFilter.location = (250,0)
    n_layerEnable.location = (250,-250)
    
    return globalFilterOpacity

def create_PLFilters(pMainGroup):
    
    
    filterGroup = pMainGroup
    
    #INPUTS
    inputOpacityGlobalFilter = filterGroup.nodes["MT_OpacityGlobalFiler"].outputs["Value"]
    inputTexColor = filterGroup.nodes["MT_TexColor"].outputs["Color"]
    inputColorBelow = filterGroup.nodes["MT_LayerInput"].outputs["Color Below"]
    inputAlphaBelow = filterGroup.nodes["MT_LayerInput"].outputs["Alpha Below"]
    
    #---------- FILTERS -------------------
    
    #FRAME LAYOUT
    n_filterFrame = filterGroup.nodes.new('NodeFrame')
    n_filterFrame.name = "MT_FrameClippingMaskFilters"
    n_filterFrame.label = "Clipping Mask Filters"
    
    #REROUTES
    n_filterRerouteIN = filterGroup.nodes.new('NodeReroute')
    n_filterRerouteIN.name = "MT_filtersColorInput"
    n_filterRerouteIN.label = "Filters Input"
    n_filterRerouteIN.parent = n_filterFrame
    
    n_filterRerouteOUT = filterGroup.nodes.new('NodeReroute')
    n_filterRerouteOUT.name = "MT_filtersColorOutput"
    n_filterRerouteOUT.label = "Filters Output"
    n_filterRerouteOUT.parent = n_filterFrame

    
    #GLOBAL FILTER LAYER
    n_globalFilter = filterGroup.nodes.new('ShaderNodeMix')
    n_globalFilter.name = "MT_globalFilterSwitcher"
    n_globalFilter.label = "Global Filter Switcher"
    n_globalFilter.data_type = "RGBA" 
    n_globalFilter.inputs["Factor"].default_value = 0
    n_globalFilter.clamp_result = True
    n_globalFilter.clamp_factor = True
    
    n_globalFilter.parent = n_filterFrame
    
    
    #LINKS
    filterGroup.links.new(inputOpacityGlobalFilter, n_globalFilter.inputs[0])
    filterGroup.links.new(inputTexColor, n_globalFilter.inputs[6])
    filterGroup.links.new(inputColorBelow, n_globalFilter.inputs[7])
    
    filterGroup.links.new(n_globalFilter.outputs[2], n_filterRerouteIN.inputs[0])
    filterGroup.links.new(n_filterRerouteIN.outputs[0], n_filterRerouteOUT.inputs[0])
    
    #POSITIONS
    n_filterRerouteIN.location = (200,0)
    n_filterRerouteOUT.location = (400,0)
    n_globalFilter.location = (-100, 0)
    n_filterFrame.location = (600, 500)

    return filterGroup


def create_PLColorOutput(pMainGroup):
    
    colorOutput = pMainGroup
    links = colorOutput.links
    
    #INPUT 
    inputColorBelow = colorOutput.nodes["MT_LayerInput"].outputs["Color Below"]
    inputLayerEnabled = colorOutput.nodes["MT_LayerInput"].outputs["Enabled"]
    inputTexColor = colorOutput.nodes["MT_TexColor"].outputs["Color"]
    inputGlobalFilter = colorOutput.nodes["MT_OpacityGlobalFiler"].outputs[0]
    inputFilterOutput = colorOutput.nodes["MT_filtersColorOutput"].outputs[0]
    inputColorOpacity = colorOutput.nodes["MT_ColorLayerOpacity"].outputs[0]
    inputColorEnabled = colorOutput.nodes["MT_ColorLayerOpacity"].inputs["Enabled"]
    inputNodeLayerAlpha = colorOutput.nodes["MT_MixColorAndMaskAlphas"].outputs[2]
    
    
    #OUTPUT FRAME
    n_outputFrame = colorOutput.nodes.new('NodeFrame')
    n_outputFrame.name = "MT_FrameColorOutput"
    n_outputFrame.label = "Frame Color Output"
    
    #MIX BLEND MODE
    n_blendMode = colorOutput.nodes.new('ShaderNodeMix')
    n_blendMode.name = "MT_layerBlendMode"
    n_blendMode.label = "Layer Blend Mode"
    n_blendMode.data_type = "RGBA" 
    n_blendMode.inputs["Factor"].default_value = 0
    n_blendMode.clamp_result = True
    n_blendMode.clamp_factor = True
    
    n_blendMode.parent = n_outputFrame
    
    #USE COLOR BELOW?
    n_useColorBelow = colorOutput.nodes.new('ShaderNodeMix')
    n_useColorBelow.name = "MT_useColorBelow"
    n_useColorBelow.label = "Use Color Below"
    n_useColorBelow.data_type = "RGBA" 
    n_useColorBelow.inputs["Factor"].default_value = 1
    n_useColorBelow.clamp_result = True
    n_useColorBelow.clamp_factor = True
    
    n_useColorBelow.parent = n_outputFrame
    
    #GLOBAL FILTER?
    n_isGlobalFilter = colorOutput.nodes.new('ShaderNodeMix')
    n_isGlobalFilter.name = "MT_useGlobalFilter"
    n_isGlobalFilter.label = "Use Global Filter"
    n_isGlobalFilter.data_type = "RGBA" 
    n_isGlobalFilter.inputs["Factor"].default_value = 0
    n_isGlobalFilter.clamp_result = True
    n_isGlobalFilter.clamp_factor = True
    
    n_isGlobalFilter.parent = n_outputFrame
    
    #PARENT
    
    n_colorLayerOpacity = colorOutput.nodes["MT_ColorLayerOpacity"]
    n_colorLayerOpacity.parent = n_outputFrame
    
    #POSITIONS
    n_outputFrame.location = (600, 0)
    n_blendMode.location = (200, 0)
    n_useColorBelow.location = (400, 0)
    n_isGlobalFilter.location = (600, 0)
    
    #------------ LINKS -------------#
    
    #LINK BLEND MODE
    links.new(inputColorBelow, n_blendMode.inputs[6])
    links.new(inputFilterOutput, n_blendMode.inputs[7])
    links.new(inputColorOpacity, n_blendMode.inputs["Factor"])
    
    #LINK USE COLOR BELOW
    links.new(n_blendMode.outputs[2], n_useColorBelow.inputs[7])
    links.new(inputColorBelow, n_useColorBelow.inputs[6])
    links.new(inputNodeLayerAlpha, n_useColorBelow.inputs["Factor"])
    #links.new(inputUseColorBelow, n_useColorBelow.inputs["Factor"])
    
    #LINK GLOBAL FILTER
    links.new(n_useColorBelow.outputs[2], n_isGlobalFilter.inputs[6])
    links.new(inputFilterOutput, n_isGlobalFilter.inputs[7])
    links.new(inputGlobalFilter, n_isGlobalFilter.inputs["Factor"])
    
    #COLOR ENABLED
    links.new(inputLayerEnabled, inputColorEnabled)
    
    #SOCKET RETURN
    colorOutputSocket = n_isGlobalFilter.outputs[2]
    
    return colorOutputSocket

def create_PLAlphaOutput(pMainGroup):
    
    alphaOutput = pMainGroup
    links = alphaOutput.links
    
    #INPUTS
    inputAlphaBelow = alphaOutput.nodes["MT_LayerInput"].outputs["Alpha Below"]
    inputAlphaOpacity = alphaOutput.nodes["MT_AlphaLayerOpacity"].outputs[0]
    inputAlphaEnabled = alphaOutput.nodes["MT_AlphaLayerOpacity"].inputs["Enabled"]
    inputLayerEnabled = alphaOutput.nodes["MT_LayerInput"].outputs["Enabled"]
    inputGlobalFilter = alphaOutput.nodes["MT_OpacityGlobalFiler"].outputs[0]
    
    

    #OUTPUT FRAME
    n_outputFrame = alphaOutput.nodes.new('NodeFrame')
    n_outputFrame.name = "MT_FrameAlphaOutput"
    n_outputFrame.label = "Frame Alpha Output"
    
    
    #ADD ALPHA MASKS
    n_addMasks = alphaOutput.nodes.new('ShaderNodeMix')
    n_addMasks.name = "MT_AddAlphas"
    n_addMasks.label = "Add Layer Alphas"
    n_addMasks.data_type = "RGBA" 
    n_addMasks.inputs["Factor"].default_value = 1
    n_addMasks.clamp_result = True
    n_addMasks.clamp_factor = True
    n_addMasks.blend_type = "ADD"
    
    n_addMasks.parent = n_outputFrame
    
    #USE ALPHA BELOW?
    n_useAlphaBelow = alphaOutput.nodes.new('ShaderNodeMix')
    n_useAlphaBelow.name = "MT_useAlphaBelow"
    n_useAlphaBelow.label = "Use Alpha Below"
    n_useAlphaBelow.data_type = "RGBA" 
    n_useAlphaBelow.inputs["Factor"].default_value = 1
    n_useAlphaBelow.clamp_result = True
    n_useAlphaBelow.clamp_factor = True
    
    n_useAlphaBelow.parent = n_outputFrame
    
    #GLOBAL FILTER?
    n_isGlobalFilter = alphaOutput.nodes.new('ShaderNodeMix')
    n_isGlobalFilter.name = "MT_useAlphaGlobalFilter"
    n_isGlobalFilter.label = "Use Alpha Global Filter"
    n_isGlobalFilter.data_type = "RGBA" 
    n_isGlobalFilter.inputs["Factor"].default_value = 0
    n_isGlobalFilter.clamp_result = True
    n_isGlobalFilter.clamp_factor = True
    
    n_isGlobalFilter.parent = n_outputFrame
    
    #PARENT
    n_alphaLayerOpacity = alphaOutput.nodes["MT_AlphaLayerOpacity"]
    n_alphaLayerOpacity.parent = n_outputFrame
    
    #POSITIONS
    n_outputFrame.location = (600, -300)
    n_addMasks.location = (200, 0)
    n_useAlphaBelow.location = (400, 0)
    n_isGlobalFilter.location = (600, 0)
    
    
    #------------ LINKS -------------#
    
    #LINK BLEND MODE
    links.new(inputAlphaOpacity, n_addMasks.inputs[6])
    links.new(inputAlphaBelow, n_addMasks.inputs[7])

    
    #LINK USE COLOR BELOW
    links.new(n_addMasks.outputs[2], n_useAlphaBelow.inputs[7])
    links.new(inputAlphaOpacity, n_useAlphaBelow.inputs[6])
    
    #ALPHA ENABLED
    links.new(inputLayerEnabled, inputAlphaEnabled)
    
    #LINK GLOBAL FILTER
    links.new(n_useAlphaBelow.outputs[2], n_isGlobalFilter.inputs[6])
    links.new(inputAlphaBelow, n_isGlobalFilter.inputs[7])
    links.new(inputGlobalFilter, n_isGlobalFilter.inputs["Factor"])
    
    #SOCKET RETURN
    alphaOutputSocket = n_isGlobalFilter.outputs[2]
    
    return alphaOutputSocket

def create_PLOutputs(pMainGroup, pColorOut, pAlphaOut):
    
    mt_node = pMainGroup
    
    #OUTPUT NODE
    n_layerOutput = mt_node.nodes.new('NodeGroupOutput')
    n_layerOutput.name = "MT_LayerOutput"
    n_layerOutput.label = 'Layer Output'
    
    outputColor = mt_node.outputs.new('NodeSocketColor','Color')
    outputAlpha = mt_node.outputs.new('NodeSocketColor','Alpha')
    
    #LINKS
    mt_node.links.new(pColorOut, n_layerOutput.inputs["Color"])
    mt_node.links.new(pAlphaOut, n_layerOutput.inputs["Alpha"])
    
    #POSITION
    n_layerOutput.location = (2000,0)
    
    return n_layerOutput
 
def create_paintLayerType():
    
    #------------- CREATE GROUP PAINTING LAYER------------------#
    
    mt_node = bpy.data.node_groups.new('MTPaintLayer', 'ShaderNodeTree')
    
    
        
    # ---------- CREATE INPUTS ------------------ #
    
    inputs = create_PLInputs(mt_node)
    inputLayerOpacity = inputs[0]
    inputGlobalFilter = inputs[1]
    inputLayerEnabled = inputs[2]
    inputColorBelow = inputs[3]
    inputColorAlpha = inputs[4]
     
    #----------- OPACITY CONTROL WITH GLOBAL FILTER ------------------------#
    
    globalFilterOpacity = create_PLGlobalFilterOpacity(mt_node)
    
    # ------------ TEXTURES  ------------------------- #
    
    plTextures = create_PLTextures(mt_node)
    n_colorTexture = plTextures[0]
    n_colorAlpha = plTextures[1]
    
    #----------- LAYER OPACITY SYSTEM GROUP ------------------ #
    
    paintLayerOpacityGroup = create_PLOpacityGroup() 
    
    # ------------ LAYER CORE SYSTEM ---------------------------- #
    
    layerOpacitySystem = create_PLOpacityControls(mt_node, paintLayerOpacityGroup.name)
    
    # ------------- LAYER FILTERS ----------------------#
    
    layerFilters = create_PLFilters(mt_node)
    
    
    
    # ------------ OUTPUTS ------------------------------- #
    
    layerColorOutput = create_PLColorOutput(mt_node)
    layerAlphaOutput = create_PLAlphaOutput(mt_node)
    
    outputs = create_PLOutputs(mt_node, layerColorOutput,layerAlphaOutput )
    
    return mt_node.name


#create_paintLayerType()

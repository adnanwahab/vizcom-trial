







# Work Log Feb 11 - fabric.js + segment
1. 9am used original cup at https://cgi-tools.dev/fabric
2. 12:30 got segment-anything2 working on cup - https://github.com/adnanwahab/vizcom-trial/blob/main/sam2/3. notebooks/image_predictor_example.ipynb





# vizcom-trial
[text](https://cgi-tools.dev/)


```bash
cd sam2
# mamba env create -f environment.yml
mamba create -n sam2 python=3.9 -y
mamba activate sam2
mamba install fastapi uvicorn numpy pillow -c conda-forge
mamba install pytorch torchvision torchaudio cudatoolkit=11.8 -c pytorch
pip install -e .
uvicorn script:app --reload --port 8000
```



# Prior art
1. [text](https://threejs.org/examples/?q=texture#webgl_materials_texture_canvas)
2. [text](https://threejs.org/examples/?q=texture#webgl_materials_texture_partialupdate)
3. [text](https://threejs.org/examples/?q=texture#webgpu_textures_partialupdate)
4. [text](https://threejs.org/examples/?q=texture#webgpu_compute_texture)


Detailed Feature Requirements:

1. Image-to-Mockup Conversion
The core of this feature is a conversion system that transforms 2D images into 3D mockup-ready models. For the POC, implement either:
    
    Manual Selection Approach:
    
    - Create an intuitive interface for users to select specific areas of the image
    
    OR
    
    Automated Segmentation Approach:
    
    - Integrate a segmentation model (e.g., Segment Anything)
    - Automatically identify distinct areas of the garment
    - Generate appropriate 3D geometry based on segmented regions
2. Material Application System
    - Implement drag-and-drop functionality for various content types:
        - Image files (JPG, PNG, etc.)
            - Material textures
            - Vector logos
            - Text elements
    - Create an intelligent wrapping system that:
        - Automatically conforms materials to the 3D surface
        - Maintains proper perspective and scaling
        - Handles surface deformation naturally
    - Provide precise controls for:
        - Scale adjustment
        - Rotation

Technical Implementation Options:

1. Vizcom Studio Integration (Preferred Approach)
    - Leverage existing Vizcom infrastructure
    - Direct integration with user workflows
2. Standalone Three.js Demo

### Quality Benchmarks:

- Surface wrapping should maintain texture integrity across curved surfaces
- UI response time should feel immediate (<100ms) for basic interactions
- Complex operations (3D conversion) should complete within reasonable time (<5s)
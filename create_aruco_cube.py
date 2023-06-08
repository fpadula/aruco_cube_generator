import importSVG
import numpy as np

# Parameters:
# cube_size = 30
marker_size = 60
marker_dict = 4
marker_height = 1
file_list = [
    "C:/Users/fpadula/Projects/Fiducials/aruco_cube_generator/aruco_svgs/4x4_1000-10.svg",
    "C:/Users/fpadula/Projects/Fiducials/aruco_cube_generator/aruco_svgs/4x4_1000-11.svg",
    "C:/Users/fpadula/Projects/Fiducials/aruco_cube_generator/aruco_svgs/4x4_1000-12.svg",
    "C:/Users/fpadula/Projects/Fiducials/aruco_cube_generator/aruco_svgs/4x4_1000-13.svg",
    "C:/Users/fpadula/Projects/Fiducials/aruco_cube_generator/aruco_svgs/4x4_1000-14.svg",
    "C:/Users/fpadula/Projects/Fiducials/aruco_cube_generator/aruco_svgs/4x4_1000-15.svg",
]
faces = ["A", "B", "C", "D", "E", "F"]
# mounting_hole_diameter = 4
# mounting_hole_depth = 4
################################


# marker_bit_size = cube_size / (marker_dict + 4)
# marker_size = marker_bit_size * (marker_dict + 2)

marker_bit_size = marker_size / (marker_dict + 2)
cube_size = marker_bit_size * (marker_dict + 4)
with open(
    "C:/Program Files/FreeCAD 0.20/data/Mod/Start/StartPage/LoadNew.py"
) as file:
    exec(file.read())

document = App.getDocument("Unnamed")
cube = document.addObject("Part::Box", "Cube")
cube.Label = "Cube"
cube.Width = f"{cube_size} mm"
cube.Height = f"{cube_size} mm"
cube.Length = f"{cube_size} mm"

# Defining cut placements:
cut_placements = [
    App.Placement(
        App.Vector(marker_bit_size, 0.00, marker_bit_size),
        App.Rotation(App.Vector(0.00, 0.00, 1.00), 0.00),
    ),
    App.Placement(
        App.Vector(
            marker_bit_size, cube_size - marker_height, marker_bit_size
        ),
        App.Rotation(App.Vector(0.00, 0.00, 1.00), 0.00),
    ),
    App.Placement(
        App.Vector(marker_height, marker_bit_size, marker_bit_size),
        App.Rotation(App.Vector(0.00, 0.00, 1.00), 90.00),
    ),
    App.Placement(
        App.Vector(cube_size, marker_bit_size, marker_bit_size),
        App.Rotation(App.Vector(0.00, 0.00, 1.00), 90.00),
    ),
    App.Placement(
        App.Vector(marker_bit_size, marker_bit_size, cube_size),
        App.Rotation(App.Vector(1.00, 0.00, 0.00), -90.00),
    ),
    App.Placement(
        App.Vector(marker_bit_size, marker_bit_size, marker_height),
        App.Rotation(App.Vector(1.00, 0.00, 0.00), -90.00),
    ),
]

# Creating box to cut space for marker
for placement, face in zip(cut_placements, faces):
    box_name = f"BoxCut{face}"
    cut_name = f"Cut{face}"

    cut_box = App.ActiveDocument.addObject("Part::Box", box_name)
    cut_box.Label = f"CutCube{face}"

    # box_obj = FreeCAD.getDocument("Unnamed").getObject(box_name)

    cut_box.Width = f"{marker_height} mm"
    cut_box.Height = f"{marker_size} mm"
    cut_box.Length = f"{marker_size} mm"

    cut_box.Placement = placement
    # continue
    cut = App.activeDocument().addObject("Part::Cut", cut_name)

    cut.Base = cube
    cut.Tool = cut_box
    cube.Visibility = False
    cut_box.Visibility = False
    cut.ViewObject.ShapeColor = getattr(
        cube.getLinkedObject(True).ViewObject,
        "ShapeColor",
        cut.ViewObject.ShapeColor,
    )
    cut.ViewObject.DisplayMode = getattr(
        cube.getLinkedObject(True).ViewObject,
        "DisplayMode",
        cut.ViewObject.DisplayMode,
    )
    App.ActiveDocument.recompute()
    cube = cut


# Adding markers
marker_placements = [
    App.Placement(
        App.Vector(
            marker_bit_size, marker_height, cube_size - marker_bit_size
        ),
        App.Rotation(App.Vector(1.00, 0.00, 0.00), 90.00),
    ),
    App.Placement(
        App.Vector(
            cube_size - marker_height,
            marker_bit_size,
            cube_size - marker_bit_size,
        ),
        App.Rotation(90.0, 0.0, 90.00),
        App.Vector(0, 0, 0),
    ),
    App.Placement(
        App.Vector(
            cube_size - marker_bit_size,
            cube_size - marker_height,
            cube_size - marker_bit_size,
        ),
        App.Rotation(180.0, 0.0, 90.00),
        App.Vector(0, 0, 0),
    ),
    App.Placement(
        App.Vector(
            marker_height,
            cube_size - marker_bit_size,
            cube_size - marker_bit_size,
        ),
        App.Rotation(-90.0, 0.0, 90.00),
        App.Vector(0, 0, 0),
    ),
    App.Placement(
        App.Vector(
            marker_bit_size,
            cube_size - marker_bit_size,
            cube_size - marker_height,
        ),
        App.Rotation(0.0, 0.0, 0.00),
        App.Vector(0, 0, 0),
    ),
    App.Placement(
        App.Vector(
            marker_bit_size,
            cube_size - marker_bit_size,
            marker_height,
        ),
        App.Rotation(0.0, 0.0, 0.00),
        App.Vector(0, 0, 0),
    ),
]
extrusion_dirs = [
    App.Vector(0.0, -1.0, 0.0),
    App.Vector(1.0, 0.0, 0.0),
    App.Vector(0.0, 1.0, 0.0),
    App.Vector(-1.0, 0.0, 0.0),
    App.Vector(0.0, 0.0, 1.0),
    App.Vector(0.0, 0.0, -1.0),
]

# faces = faces
# faces = ["A", "B", "C", "D", "E"]
rect_count = 1
for marker_name, placement, extrusion_dir, file_name in zip(
    faces, marker_placements, extrusion_dirs, file_list
):
    # Loading SVG
    importSVG.insert(file_name, "Unnamed")
    document.removeObject("Rectangle")
    # Extruding aruco segments
    extrusion_list = []
    while True:
        if rect_count >= 100:
            obj_name = f"Rectangle{rect_count}"
        elif rect_count >= 10:
            obj_name = f"Rectangle0{rect_count}"
        else:
            obj_name = f"Rectangle00{rect_count}"

        segment = document.getObject(obj_name)
        if segment is None:
            break
        rect_count += 1
        segment.Placement = placement

        extrusion = document.addObject(
            "Part::Extrusion", obj_name + "_extrusion"
        )
        extrusion_list.append(extrusion)
        extrusion.Base = segment
        extrusion.DirMode = "Custom"
        extrusion.Dir = extrusion_dir
        extrusion.DirLink = None
        extrusion.LengthFwd = 1.0
        extrusion.LengthRev = 0.0
        extrusion.Solid = False
        extrusion.Reversed = False
        extrusion.Symmetric = False
        extrusion.TaperAngle = 0.000000000000000
        extrusion.TaperAngleRev = 0.000000000000000
        extrusion.ViewObject.ShapeColor = getattr(
            segment.getLinkedObject(True).ViewObject,
            "ShapeColor",
            extrusion.ViewObject.ShapeColor,
        )
        extrusion.ViewObject.LineColor = getattr(
            segment.getLinkedObject(True).ViewObject,
            "LineColor",
            extrusion.ViewObject.LineColor,
        )
        extrusion.ViewObject.PointColor = getattr(
            segment.getLinkedObject(True).ViewObject,
            "PointColor",
            extrusion.ViewObject.PointColor,
        )
        segment.Visibility = False

    # Combining all segments into one
    fused_extrusions = App.activeDocument().addObject(
        "Part::MultiFuse", f"Fusion_{marker_name}"
    )
    fused_extrusions.Shapes = extrusion_list
    for extrusion in extrusion_list:
        extrusion.Visibility = False
    fused_extrusions.ViewObject.ShapeColor = getattr(
        extrusion_list[0].getLinkedObject(True).ViewObject,
        "ShapeColor",
        fused_extrusions.ViewObject.ShapeColor,
    )
    fused_extrusions.ViewObject.DisplayMode = getattr(
        extrusion_list[0].getLinkedObject(True).ViewObject,
        "DisplayMode",
        fused_extrusions.ViewObject.DisplayMode,
    )

    fused_cube = document.addObject(
        "Part::MultiFuse", f"Fusion_with_cube_{marker_name}"
    )
    fused_cube.Shapes = [fused_extrusions, cube]
    fused_extrusions.Visibility = False
    cube.Visibility = False
    fused_cube.ViewObject.ShapeColor = getattr(
        fused_extrusions.getLinkedObject(True).ViewObject,
        "ShapeColor",
        fused_cube.ViewObject.ShapeColor,
    )
    fused_cube.ViewObject.DisplayMode = getattr(
        fused_extrusions.getLinkedObject(True).ViewObject,
        "DisplayMode",
        fused_cube.ViewObject.DisplayMode,
    )

    cube = fused_cube
    App.ActiveDocument.recompute()


# # Adding mounting hole
# cut_cylinder = document.addObject("Part::Cylinder", "Cylinder")
# cut_cylinder.Label = "Cylinder"
# cut_cylinder.Radius = mounting_hole_diameter / 2
# cut_cylinder.Height = mounting_hole_depth
# cut_cylinder.Placement = App.Placement(
#     App.Vector(cube_size / 2, cube_size / 2, 0.00),
#     App.Rotation(App.Vector(0.00, 0.00, 1.00), 0.00),
# )

# # Begin command Part_Cut
# cut_obj = document.addObject("Part::Cut", "Cut")
# cut_obj.Base = cube
# cut_obj.Tool = cut_cylinder
# cube.Visibility = False
# cut_cylinder.Visibility = False
# cut_obj.ViewObject.ShapeColor = getattr(
#     cube.getLinkedObject(True).ViewObject,
#     "ShapeColor",
#     cut_obj.ViewObject.ShapeColor,
# )
# cut_obj.ViewObject.DisplayMode = getattr(
#     cube.getLinkedObject(True).ViewObject,
#     "DisplayMode",
#     cut_obj.ViewObject.DisplayMode,
# )
# App.ActiveDocument.recompute()
# # End command Part_Cut

# marker_H = {
#     "top_left": np.eye(4),
#     "top_right": np.
# }
# # Printing cube board definition:
# for marker_name in faces:
#     print(f"{marker_name}:")
#     print()

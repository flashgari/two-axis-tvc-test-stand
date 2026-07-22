include <common.scad>

// Rev A hard-stop block.
// Print flat; use two mirrored copies per constrained axis as needed.

difference() {
    rounded_plate([24, 10, 10], 2);
    translate([-6, 0, 0])
        cylinder(h=11, d=m3_clearance_d, center=true);
    translate([6, 0, 0])
        cylinder(h=11, d=m3_clearance_d, center=true);
}

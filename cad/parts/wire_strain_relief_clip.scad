include <common.scad>

// Rev A wire strain-relief clip.
// Print flat. Use near rotation axes to keep wire stiffness from becoming a torque spring.

difference() {
    union() {
        rounded_plate([28, 12, 5], 2);
        translate([0, 0, 5])
            rounded_plate([22, 8, 5], 2);
    }

    // Wire channel.
    translate([0, 0, 5])
        rotate([90, 0, 0])
            cylinder(h=14, d=4.0, center=true);

    // Mount screw.
    translate([0, 0, 0])
        cylinder(h=12, d=m3_clearance_d, center=true);
}

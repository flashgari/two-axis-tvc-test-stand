include <common.scad>

// Rev A outer yaw frame.
// Print on its back face if possible; add supports only if needed.

difference() {
    union() {
        translate([0, -outer_w/2, outer_h/2])
            cube([outer_depth, wall_t, outer_h], center=true);
        translate([0, outer_w/2, outer_h/2])
            cube([outer_depth, wall_t, outer_h], center=true);
        translate([0, 0, outer_h])
            cube([outer_depth, outer_w + wall_t, wall_t], center=true);

        // Local bearing/bushing bosses for pitch shaft support.
        for (y=[-outer_w/2, outer_w/2])
            translate([0, y, outer_h/2])
                rotate([90, 0, 0])
                    cylinder(h=wall_t + 6, d=bearing_d + 8, center=true);
    }

    // Pitch-axis shaft clearance.
    translate([0, 0, outer_h/2])
        shaft_clearance(outer_w + 20);

    // Lightening/inspection window.
    translate([0, 0, outer_h*0.58])
        cube([outer_depth + 1, outer_w - 28, outer_h*0.35], center=true);
}

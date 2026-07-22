include <common.scad>

// Rev A inner pitch/nozzle carrier.
// Print so the shaft features have good perimeter strength.

difference() {
    union() {
        translate([0, -inner_w/2, inner_h/2])
            cube([wall_t, wall_t, inner_h], center=true);
        translate([0, inner_w/2, inner_h/2])
            cube([wall_t, wall_t, inner_h], center=true);
        translate([0, 0, inner_h])
            cube([wall_t, inner_w + wall_t, wall_t], center=true);

        // IMU pad on controlled moving body.
        translate([0, 0, inner_h + 8])
            rotate([0, 90, 0])
                imu_pad();

        // Nozzle mounting boss.
        translate([8, 0, inner_h/2])
            rotate([0, 90, 0])
                cylinder(h=14, d=nozzle_d + 8, center=true);
    }

    // Pitch shaft clearance.
    translate([0, 0, inner_h/2])
        shaft_clearance(inner_w + 22);

    // Nozzle attachment clearance.
    translate([8, 0, inner_h/2])
        rotate([0, 90, 0])
            cylinder(h=16, d=nozzle_d + 1.0, center=true);
}

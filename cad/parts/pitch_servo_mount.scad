include <common.scad>

// Rev A pitch servo mount.
// Print flat, then mount to the outer yaw frame.

difference() {
    union() {
        servo_mount_plate();

        // Frame attachment ears.
        translate([0, -(servo_mount_span_y/2 + 14), 0])
            rounded_plate([servo_mount_span_x + 22, 12, mount_t], 2);
        translate([0, servo_mount_span_y/2 + 14, 0])
            rounded_plate([servo_mount_span_x + 22, 12, mount_t], 2);
    }

    for (x=[-25, 25])
        for (y=[-(servo_mount_span_y/2 + 14), servo_mount_span_y/2 + 14])
            translate([x, y, 0])
                cylinder(h=mount_t + 1, d=m3_clearance_d, center=true);
}

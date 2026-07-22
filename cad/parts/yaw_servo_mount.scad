include <common.scad>

// Rev A yaw servo mount.
// Print flat with slots in the XY plane.

difference() {
    union() {
        servo_mount_plate();

        // Alignment rail references for the HS-625MG body.
        translate([0, -(servo_w/2 + 4), mount_t/2 + 4])
            cube([servo_l + 8, 4, 8], center=true);
        translate([0, servo_w/2 + 4, mount_t/2 + 4])
            cube([servo_l + 8, 4, 8], center=true);
    }

    // Keep the servo body area open for fit tolerance.
    translate([0, 0, mount_t/2 + servo_h/2])
        servo_body_clearance(2);
}

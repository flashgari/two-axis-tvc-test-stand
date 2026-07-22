// Shared Rev A CAD parameters and helper modules.
// Units: millimeters.

$fn = 48;

// Hitec HS-625MG vendor baseline. Verify with calipers before final print.
servo_l = 40.6;
servo_w = 19.8;
servo_h = 37.8;
spline_d = 6.0;
spline_h = 5.0;
servo_mount_slot_l = 9.0;
servo_mount_slot_w = 3.4;
servo_mount_span_x = 49.5;
servo_mount_span_y = 27.5;

// Rev A structure.
base_l = 160;
base_w = 120;
base_t = 6;
wall_t = 6;
mount_t = 5;
outer_w = 95;
outer_h = 95;
outer_depth = 16;
inner_w = 55;
inner_h = 72;
nozzle_l = 85;
nozzle_d = 24;
imu_l = 28;
imu_w = 22;
bearing_d = 8.0;
shaft_d = 4.0;

// Manufacturing assumptions.
m3_clearance_d = 3.4;
bench_fastener_d = 5.0;
fillet_r = 3.0;

module rounded_plate(size_xyz, r=3) {
    hull() {
        for (x=[-size_xyz[0]/2+r, size_xyz[0]/2-r])
            for (y=[-size_xyz[1]/2+r, size_xyz[1]/2-r])
                translate([x, y, 0])
                    cylinder(h=size_xyz[2], r=r, center=true);
    }
}

module slotted_hole(slot_l, slot_w, h=2) {
    hull() {
        translate([-slot_l/2 + slot_w/2, 0, 0])
            cylinder(h=h, d=slot_w, center=true);
        translate([slot_l/2 - slot_w/2, 0, 0])
            cylinder(h=h, d=slot_w, center=true);
    }
}

module servo_mount_plate() {
    difference() {
        rounded_plate([servo_mount_span_x + 18, servo_mount_span_y + 16, mount_t], 2);

        for (x=[-servo_mount_span_x/2, servo_mount_span_x/2])
            for (y=[-servo_mount_span_y/2, servo_mount_span_y/2])
                translate([x, y, 0])
                    slotted_hole(servo_mount_slot_l, servo_mount_slot_w, mount_t + 1);
    }
}

module servo_body_clearance(extra=1.0) {
    cube([servo_l + extra, servo_w + extra, servo_h + extra], center=true);
}

module shaft_clearance(h=120) {
    rotate([90, 0, 0])
        cylinder(h=h, d=shaft_d + 0.6, center=true);
}

module imu_pad() {
    difference() {
        rounded_plate([imu_l + 8, imu_w + 8, 3], 2);
        for (x=[-(imu_l/2 - 4), imu_l/2 - 4])
            for (y=[-(imu_w/2 - 4), imu_w/2 - 4])
                translate([x, y, 0])
                    cylinder(h=4, d=2.2, center=true);
    }
}

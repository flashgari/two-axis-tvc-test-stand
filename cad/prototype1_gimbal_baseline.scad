// Prototype 1 two-axis TVC gimbal concept.
// Units: millimeters.
// This is a parametric layout model, not a manufacturing-ready drawing.

$fn = 48;

// Servo envelope: Hitec HS-625MG vendor baseline.
servo_l = 40.6;
servo_w = 19.8;
servo_h = 37.8;
spline_d = 6.0;
spline_h = 5.0;
servo_mount_slot_l = 9.0;
servo_mount_slot_w = 3.4;
servo_mount_span_x = 49.5; // Rev A standard-servo placeholder; verify on arrival.
servo_mount_span_y = 27.5; // Rev A standard-servo placeholder; verify on arrival.

// Structural assumptions.
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
bearing_d = 8.0; // placeholder for small supported shaft/bushing option.
shaft_d = 4.0;

// Display angles for concept visualization.
yaw_demo_deg = 0;
pitch_demo_deg = 10;

module rounded_plate(size_xyz, r=3) {
    hull() {
        for (x=[-size_xyz[0]/2+r, size_xyz[0]/2-r])
            for (y=[-size_xyz[1]/2+r, size_xyz[1]/2-r])
                translate([x, y, 0])
                    cylinder(h=size_xyz[2], r=r, center=true);
    }
}

module servo_envelope(label_side=1) {
    color([0.15, 0.35, 0.95, 0.35])
        cube([servo_l, servo_w, servo_h], center=true);

    // Output spline reference.
    translate([servo_l/2 - 10, 0, servo_h/2 + spline_h/2])
        color([0.1, 0.1, 0.1])
            cylinder(h=spline_h, d=spline_d, center=true);

    // Mounting ears, approximate envelope only.
    for (x=[-servo_l/2 - 3, servo_l/2 + 3])
        translate([x, 0, servo_h*0.15])
            color([0.1, 0.1, 0.1, 0.35])
                cube([6, servo_w + 9, 3], center=true);

    // Wire-exit reference.
    translate([-servo_l/2 - 8, label_side*(servo_w/2 + 3), -servo_h/2 + 6])
        color([0.4, 0.4, 0.4])
            cylinder(h=18, d=2, center=true, $fn=12);
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
        color([0.12, 0.12, 0.12, 0.35])
            cube([servo_mount_span_x + 18, servo_mount_span_y + 16, mount_t], center=true);

        // Slotted mount holes tolerate printed error and servo-to-servo variation.
        for (x=[-servo_mount_span_x/2, servo_mount_span_x/2])
            for (y=[-servo_mount_span_y/2, servo_mount_span_y/2])
                translate([x, y, 0])
                    slotted_hole(servo_mount_slot_l, servo_mount_slot_w, mount_t + 1);
    }
}

module base_plate() {
    color([0.82, 0.82, 0.82])
        rounded_plate([base_l, base_w, base_t], 4);

    // Bench clamp/fastener references.
    for (x=[-base_l/2 + 15, base_l/2 - 15])
        for (y=[-base_w/2 + 15, base_w/2 - 15])
            translate([x, y, base_t/2 + 0.2])
                color([0.08, 0.08, 0.08])
                    cylinder(h=1.0, d=5, center=true);
}

module yaw_frame() {
    color([0.05, 0.65, 0.45, 0.75]) {
        translate([0, -outer_w/2, outer_h/2])
            cube([outer_depth, wall_t, outer_h], center=true);
        translate([0, outer_w/2, outer_h/2])
            cube([outer_depth, wall_t, outer_h], center=true);
        translate([0, 0, outer_h])
            cube([outer_depth, outer_w + wall_t, wall_t], center=true);
    }
}

module pitch_carrier() {
    color([0.85, 0.55, 0.1, 0.8]) {
        translate([0, -inner_w/2, inner_h/2])
            cube([wall_t, wall_t, inner_h], center=true);
        translate([0, inner_w/2, inner_h/2])
            cube([wall_t, wall_t, inner_h], center=true);
        translate([0, 0, inner_h])
            cube([wall_t, inner_w + wall_t, wall_t], center=true);
    }

    // IMU pad on moving carrier.
    translate([0, 0, inner_h + 7])
        color([0.3, 0.0, 0.8, 0.85])
            cube([3, imu_l, imu_w], center=true);

    // Supported pitch-axis shaft reference.
    translate([0, 0, inner_h/2])
        rotate([90, 0, 0])
            color([0.05, 0.05, 0.05])
                cylinder(h=inner_w + 22, d=shaft_d, center=true);
}

module mock_nozzle() {
    rotate([0, 90, 0])
        color([0.9, 0.15, 0.12, 0.85])
            cylinder(h=nozzle_l, d1=nozzle_d*1.35, d2=nozzle_d*0.65, center=true);
}

module hard_stop_arc(radius=42) {
    // Visual references for +/-15 deg hard-stop envelope.
    for (a=[-15, 15])
        rotate([0, 0, a])
            translate([radius, 0, 42])
                color([0.85, 0.0, 0.0])
                    cube([18, 2.5, 8], center=true);
}

module gimbal_assembly() {
    translate([0, 0, base_t/2])
        yaw_frame();

    // Bearing/bushing references for supported pitch axis.
    for (y=[-outer_w/2 - 5, outer_w/2 + 5])
        translate([0, y, base_t/2 + 8 + inner_h/2])
            rotate([90, 0, 0])
                color([0.2, 0.2, 0.2, 0.7])
                    cylinder(h=4, d=bearing_d, center=true);

    rotate([0, 0, yaw_demo_deg])
        translate([0, 0, base_t/2 + 8])
            rotate([0, pitch_demo_deg, 0]) {
                pitch_carrier();
                translate([nozzle_l/2 - 8, 0, inner_h/2])
                    mock_nozzle();
            }

    hard_stop_arc();
}

base_plate();

// Yaw servo on base.
translate([-45, -base_w/2 + 22, base_t/2 + servo_h/2])
    rotate([0, 0, 0])
        servo_envelope(1);
translate([-45, -base_w/2 + 22, base_t + 2])
    servo_mount_plate();

// Pitch servo envelope shown on right side of gimbal.
translate([0, outer_w/2 + 23, base_t/2 + 45])
    rotate([90, 0, 90])
        servo_envelope(-1);
translate([0, outer_w/2 + 23, base_t/2 + 45])
    rotate([90, 0, 90])
        servo_mount_plate();

gimbal_assembly();

// Axis references.
color([0.1, 0.1, 0.1]) {
    translate([0, 0, base_t + 100])
        cylinder(h=16, d=2, center=true);
    translate([0, 0, base_t + 108])
        cylinder(h=5, d1=8, d2=0, center=true);
}

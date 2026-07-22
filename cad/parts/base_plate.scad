include <common.scad>

// Rev A base plate.
// Print flat on the bed.

difference() {
    rounded_plate([base_l, base_w, base_t], 4);

    // Bench clamp/fastener holes.
    for (x=[-base_l/2 + 15, base_l/2 - 15])
        for (y=[-base_w/2 + 15, base_w/2 - 15])
            translate([x, y, 0])
                cylinder(h=base_t + 1, d=bench_fastener_d, center=true);

    // Optional cable-tie holes for wire strain relief.
    for (x=[base_l/2 - 35, base_l/2 - 22])
        translate([x, 0, 0])
            cube([3, 16, base_t + 1], center=true);
}

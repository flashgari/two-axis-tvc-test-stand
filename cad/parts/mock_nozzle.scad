include <common.scad>

// Rev A mock nozzle.
// Print with the centerline vertical for best circularity, or horizontal for faster fit checks.

difference() {
    rotate([0, 90, 0])
        cylinder(h=nozzle_l, d1=nozzle_d*1.35, d2=nozzle_d*0.65, center=true);

    // Hollow core reduces pitch inertia while preserving visual size.
    rotate([0, 90, 0])
        cylinder(h=nozzle_l + 2, d1=nozzle_d*0.85, d2=nozzle_d*0.45, center=true);
}

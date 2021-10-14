$fs=0.5;
$fa=0.5;

boxSize=[160, 77, 40];
boxMountingHoleSize = 1.6;
boxMountingHolePlusSize = 1.9;
displayMountSize = [30.5, 28.4];

edgeScrewDistance = 7;
lidHolePts = [
	[edgeScrewDistance, edgeScrewDistance, -135],
	[boxSize.x-edgeScrewDistance, edgeScrewDistance, -45],
	[boxSize.x-edgeScrewDistance, boxSize.y-edgeScrewDistance, 45],
	[edgeScrewDistance, boxSize.y-edgeScrewDistance, 135],
];

//bottom(boxSize);
walls(boxSize);


//rotate([0, 180, 0]) 
//translate([0, 0, boxSize.z]) lid(boxSize);
//displayTest();
//raster([boxSize.x, boxSize.y]);
//rotate([0, 180, 0]) buttonMount();

//tinsert(3);
module tinsert(msize){
	
	pts = [
	[msize*cos(0), msize*sin(0)],
	[msize*cos(60), msize*sin(60)],
	[msize*cos(120), msize*sin(120)],
	[msize*cos(180), msize*sin(180)],
	[msize*cos(240), msize*sin(240)],
	[msize*cos(300), msize*sin(300)]
	];
	translate([0, 0, -15])
	difference(){
		linear_extrude(15) circle(msize+2);
		translate([0, 0, 10]) linear_extrude(10) circle(msize/2+0.15);
		translate([0, 0, -2]) linear_extrude(10) polygon(pts);
		translate([0, 0, -6]) rotate([0, 45, 0]) linear_extrude(7.5) square([10*msize, 10*msize], center=true);
	}

}

//extension(boxSize);
module extension(size){
	circleCenter = [boxSize.x/2, -1, -235/2-4];

	
	//rotate([-90, 0, 0]) linear_extrude(120) circle(10);
	difference(){
		union(){
			translate([0, 0, -size.z]) walls(size);
			difference(){
				translate([0, 0, -2]) base([size.x, size.y, 2]);				
				scale([0.8, 0.8, 8]) translate([size.x*0.2*0.5, size.y*0.2*0.5, -1]) base([size.x, size.y, 2]);
			}
			
			translate([0, 0, -size.z]) linear_extrude(size.z) hull(){
				translate([15, 0, 0]) square([10, 10]);
				translate([15, size.y-10, 0]) square([10, 10]);
				translate([5, size.y-5, 0]) circle(5);
				translate([5, 5, 0]) circle(5);
			}
			translate([0, 0, -size.z]) linear_extrude(size.z) hull(){
				translate([size.x-25, 0, 0]) square([10, 10]);
				translate([size.x-25, size.y-10, 0]) square([10, 10]);
				translate([size.x-5, size.y-5, 0]) circle(5);
				translate([size.x-5, 5, 0]) circle(5);
			}
			
		}
		// remove space for the psu-bracket
		translate([30, size.y/2, 0.1]) rotate([-90, 0, 90]) linear_extrude(20) polygon([[-8, 0], [-8, 20], [8, 20], [8, 0]]);
		//polygon([[-8, 0], [-8, 3], [0, 11], [8, 3], [8, 0]]);
		
		translate(circleCenter) rotate([0, -35.5, 0]) translate([0, 17, 123]) {
			linear_extrude(100) circle(4.5);
			translate([0, 0, -10]) linear_extrude(100) circle(2.2);
		}
		translate(circleCenter) rotate([0, -35.5, 0]) translate([0, size.y-17, 123]) {
			linear_extrude(100) circle(4.5);
			translate([0, 0, -10]) linear_extrude(100) circle(2.2);
		}
		translate(circleCenter) rotate([0, 35.5, 0]) translate([0, 17, 123]) {
			linear_extrude(100) circle(4.5);
			translate([0, 0, -10]) linear_extrude(100) circle(2.2);
		}
		translate(circleCenter) rotate([0, 35.5, 0]) translate([0, size.y-17, 123]) {
			linear_extrude(100) circle(4.5);
			translate([0, 0, -10]) linear_extrude(100) circle(2.2);
		}

		circleSize=5;
		holeSize=4.1;
		circleHeight=size.z-10;
		/*translate([0, 0, -100]) linear_extrude(92){
			translate([circleSize+2, circleSize+2]) circle(holeSize);
			translate([circleSize+2, size.y -circleSize-2]) circle(holeSize);
			translate([size.x - circleSize -2, size.y -circleSize-2]) circle(holeSize);
			translate([size.x - circleSize -2, circleSize+2]) circle(holeSize);
		}*/

		translate([0, 0, -100]) linear_extrude(110){
			translate([circleSize+2+10, circleSize+2+5]) circle(boxMountingHolePlusSize-0.4);
			translate([circleSize+2+10, size.y -circleSize-2]) circle(boxMountingHolePlusSize-0.4);
			translate([size.x - circleSize -2-10, size.y -circleSize-2]) circle(boxMountingHolePlusSize-0.4);
			translate([size.x - circleSize -2-10, circleSize+2+5]) circle(boxMountingHolePlusSize-0.4);
		}

		translate(circleCenter) rotate([-90, 0, 0]) linear_extrude(120) circle(235/2+2);

	}

}

//waxstation();
module waxstation(){
	translate([boxSize.x/2, 0, -235/2-5]) rotate([-90, 0, 0]) linear_extrude(120) circle(235/2);
	//translate([-80, -235/2-5, 0]) rotate([90, 0, 0]) linear_extrude(50) square([160, 80]);
}


module walls(size){
	wallThickness=2;
	union(){
		for (i = [0:3]){
 			mountPt = lidHolePts[i];
 			difference(){
	 			translate([mountPt.x, mountPt.y, size.z-4-15]) 
	 				rotate([0, 0, i*90])
	 					linear_extrude(15) hull(){
	 						circle(6); 
	 						translate([0, -6, 0]) square([6, 6]); 
	 						translate([-6, 0, 0]) square([6, 6]); 
	 					}
				translate([mountPt.x, mountPt.y, size.z-4-20])  linear_extrude(25) circle(1.4); 				
 			}
		}
		//for (p = lidHolePts) translate([p.x, p.y, size.z-4-15]) rotate([0, 0, 0]) 

		//linear_extrude(15) hull(){circle(6); square([6, 6]); translate([-6, -6, 0]) square([6, 6]);}
		//tinsert(3);
		difference(){
			base(size);
			translate([wallThickness, wallThickness, -1]) scale([(size.x-2*wallThickness)/size.x, (size.y-2*wallThickness)/size.y, 2]) base(size);
			difference(){
				translate([size.x-5, size.y-20, 2+17/2]) rotate([0, 90, 0]) linear_extrude(10) circle(11/2);
				translate([size.x-5, size.y-25 - 11/2 +0.6, 2+17/2]) cube([10, 10, 10], center=true);
			}
		}
	
	}
}

//psuDistance();
module psuDistance(){
	translate([-100, 0, 0])  linear_extrude(3.04) difference(){
		hull(){
			circle(6);
			translate([39, 0, 0]) circle(6);
		}
		circle(1.5);
		translate([39, 0, 0]) circle(1.5);
	} 
}
module bottom(size){

	circleSize=5;
	circleHeight=size.z-10;
	difference(){
		union(){			
			base([size.x, size.y, 2]);
			/*
			translate([circleSize+2, circleSize+2, 0]) screwMount(circleSize, 1.25, circleHeight);
			translate([circleSize+2, size.y -circleSize-2, 0]) screwMount(circleSize, 1.25, circleHeight);
			translate([size.x - circleSize -2, size.y -circleSize-2, 0]) screwMount(circleSize, 1.25, circleHeight);
			translate([size.x - circleSize -2, circleSize+2, 0]) screwMount(circleSize, 1.25, circleHeight);
			*/
			// relay
			translate([95, 1+5, 2-0.01]) {
				translate([0, 0, 0]) smallScrewMount(7);
				translate([49.5, 0, 0]) smallScrewMount(7);
				translate([0, 20, 0]) smallScrewMount(7);
				translate([49.5, 20, 0]) smallScrewMount(7);
			}
		} // union

		// PSU mounting holes	
		translate([18, 13+51/2, -1]) linear_extrude(10) circle(1.5);
		translate([18+39, 13+51/2, -1]) linear_extrude(10) circle(1.5);

		// cable hole
		hull(){
			translate([size.x/2, 20, -1]) linear_extrude(10) circle(8.5);
			translate([size.x/2, 30, -1]) linear_extrude(10) circle(8.5);			
		}

		translate([0, 0, -1])
		linear_extrude(circleHeight-6){
			translate([circleSize+2+10, circleSize+2+5]) circle(boxMountingHolePlusSize); // 2.3
			translate([circleSize+2+10, size.y -circleSize-2]) circle(boxMountingHolePlusSize);
			translate([size.x - circleSize -2-10, size.y -circleSize-2]) circle(boxMountingHolePlusSize);
			translate([size.x - circleSize -2-10, circleSize+2+5]) circle(boxMountingHolePlusSize);			
		}
	} // difference
	
	/*
	translate([93, 28, 5]) rotate([0, 0, -90]) {
		linear_extrude(12) square([24, 54]); // relay
		linear_extrude(18) square([24, 33]); // relay
	}
	translate([3, 13, 2]) color("gray")  linear_extrude(28) square([62.5+12.5, 51/2]); // PSU	
	*/
}

module base(size){
	circleSize=5;
	linear_extrude(size.z)
	hull(){
		translate([circleSize, circleSize]) circle(circleSize);
		translate([circleSize, size.y -circleSize]) circle(circleSize);
		translate([size.x - circleSize, size.y -circleSize]) circle(circleSize);
		translate([size.x - circleSize, circleSize]) circle(circleSize);
	}
}

module buttonMount(){
	difference(){

		} // difference
		union(){
			difference(){
				linear_extrude(3) square([26, 70]);
				translate([0, 0, -1]) linear_extrude(3){
					translate([7, -0.01]) square([10, 20]);
					translate([-0.01, 12]) square([20, 20]);
					translate([5, 31.9]) square([17, 18.2]);
					translate([5, 50]) square([12, 16]);
				}
				translate([0, 0, -1]) linear_extrude(5) translate([-0.01, 12]) square([5, 20]);
				translate([2.5, 6, 0]){
					translate([0, 0, -7]) smallScrew();
					translate([0, 15*2.5, -7]) smallScrew();
					translate([0, 23*2.5, -7]) smallScrew();

					translate([8*2.5, 0, -7]) smallScrew();
					translate([8*2.5, 8*2.5, -7]) smallScrew();
					translate([8*2.5, 23*2.5, -7]) smallScrew();

				}
			} // difference
			translate([5*2.5, 6+8*2.5, 0]) linear_extrude(3) circle(2);
			translate([5*2.5, 6+15*2.5, 0]) linear_extrude(3) circle(2);
		}// union


	
}

//buttonModuleBracket();
module buttonModuleBracket(){
	height = 3;
	lowHeight = 1.5;
	difference(){
		union(){
			hull(){
				translate(pcbPoint(-18, 0, 0))  linear_extrude(height) circle(4);
				translate(pcbPoint(-18, 6, 0))  linear_extrude(height) circle(4);			
			}
			
			hull(){
				translate(pcbPoint(-18, 0, 0))  linear_extrude(lowHeight) circle(4);
				translate(pcbPoint(-18, 6, 0))  linear_extrude(lowHeight) circle(4);
				translate(pcbPoint(-15, 3, 0))  linear_extrude(lowHeight) circle(4);
			}

			translate(pcbPoint(-9, 3, 0))  linear_extrude(height) circle(3.5);
			translate(pcbPoint(0, 3, 0))  linear_extrude(height) circle(3.5);
			translate(pcbPoint(9, 3, 0))  linear_extrude(height) circle(3.5);

			translate(pcbPoint(0, 3, 0)) linear_extrude(lowHeight) square([75, 8], center=true);

			hull(){
				translate(pcbPoint(18, 0, 0))  linear_extrude(lowHeight) circle(4);
				translate(pcbPoint(18, 6, 0))  linear_extrude(lowHeight) circle(4);
				translate(pcbPoint(15, 3, 0))  linear_extrude(lowHeight) circle(4);
			}
			
			hull(){
				translate(pcbPoint(18, 0, 0))  linear_extrude(height) circle(4);
				translate(pcbPoint(18, 6, 0))  linear_extrude(height) circle(4);			
			}
			translate(pcbPoint(0, 3, 0)) linear_extrude(height) square([67, 1.8], center=true);		
		}

		translate(pcbPoint(-18, 0, 10.8)) rotate([0, 180, 0]) smallScrew();
		translate(pcbPoint(-18, 6, 10.8)) rotate([0, 180, 0]) smallScrew();
		translate(pcbPoint(0, 3, 10.8)) rotate([0, 180, 0]) smallScrew();
		translate(pcbPoint(18, 0, 10.8)) rotate([0, 180, 0]) smallScrew();
		translate(pcbPoint(18, 6, 10.8)) rotate([0, 180, 0]) smallScrew();
	}
	 //translate(pcbPoint(-19, 0, 11)) rotate([0, 180, 0]) smallScrew();
}

module lid(size){
	
	displaySize = [29.4, 16.];
	displayMountToDisplayTop = 3.1;
	displayTopLength = 21-10;
	//displayMountSize = [21, 22];
	//displaySize = [24.6, 14.7];
	//displayMountToDisplayTop = 3.5;
	//displayTopLength = 20;

	circleSize=5;
	buttonStartPos = [size.x/2, 18, -1];

	difference(){
		union(){
			base([size.x, size.y, 2]);
			translate(buttonStartPos)
			translate(pcbPoint(0, -3, 1)) { // switch-base-thickness
				upSideDown = [0, 180, 0];
				// buttons mount
				translate(pcbPoint(-18, 0, 0))  rotate(upSideDown) smallScrewMount(4);
				translate(pcbPoint(-18, 6, 0))  rotate(upSideDown) smallScrewMount(4);
				translate(pcbPoint(0, 3, 0))  rotate(upSideDown) smallScrewMount(4);
				translate(pcbPoint(18, 0, 0))  rotate(upSideDown) smallScrewMount(4);
				translate(pcbPoint(18, 6, 0))  rotate(upSideDown) smallScrewMount(4);
				
				// pcb mount
				translate(pcbPoint(23, 8, 0))  rotate(upSideDown) smallScrewMount(9);
				translate(pcbPoint(25, 22, 0))  rotate(upSideDown) smallScrewMount(9);
				//translate(pcbPoint(14, 10, 0))  rotate(upSideDown) smallScrewMount(9);
				translate(pcbPoint(14, 22, 0))  rotate(upSideDown) smallScrewMount(9);

			}

			difference(){
				translate([2, 2, -4]) scale([(size.x-2*2)/size.x, (size.y-2*2)/size.y, 1]) base([size.x, size.y, 4]);
				translate([4, 4, -5]) scale([(size.x-2*4)/size.x, (size.y-2*4)/size.y, 2]) base([size.x, size.y, 4]);
			}
			/*
			screw towers
			translate([0,0,-size.z+2]) {
				translate([circleSize+2, circleSize+2, 0]) screwMount(circleSize, boxMountingHoleSize, size.z-1);
				translate([circleSize+2, size.y -circleSize-2, 0]) screwMount(circleSize, boxMountingHoleSize, size.z-1);
				translate([size.x - circleSize -2, size.y -circleSize-2, 0]) screwMount(circleSize, boxMountingHoleSize, size.z-1);
				translate([size.x - circleSize -2, circleSize+2, 0]) screwMount(circleSize, boxMountingHoleSize, size.z-1);

			}
			*/

			// lid screw houses
			for (p = lidHolePts) translate([p.x, p.y, 0]){
				translate([0, 0, -4.1]) linear_extrude(6) circle(5);
			}

			// display mounts
			
			translate([size.x/2-displayMountSize.x/2, size.y-displayTopLength+displayMountToDisplayTop, -0.799]) { 
				translate([0, 0, 0]) displayMount(); 
				translate([displayMountSize.x, 0, 0]) displayMount();
				translate([0, -displayMountSize.y, 0]) displayMount();
				translate([displayMountSize.x, -displayMountSize.y, 0]) displayMount();
				
				translate([-7, 0, 0.798-4]) smallScrewMount(4);
				translate([displayMountSize.x+7, 0, 0.798-4]) smallScrewMount(4);
				translate([-7, -displayMountSize.y, 0.798-4]) smallScrewMount(4);
				translate([displayMountSize.x+7, -displayMountSize.y, 0.798-4]) smallScrewMount(4);
				/*
				difference(){
					translate([-2.2, -displayMountSize.y-5.0+0.2, 0.799+0.2]) linear_extrude(2-0.2) square([displayMountSize.x+4.4, 7]);
					translate([0, -displayMountSize.y, -1]) linear_extrude(10) circle(1);
					translate([displayMountSize.x, -displayMountSize.y, -1]) linear_extrude(10) circle(1);
				}
				*/
			} 
			
		}

		// cutout for lid screws
		
		for (p = lidHolePts) translate([p.x, p.y, 0]){
			translate([0, 0, -1.99]) linear_extrude(4) circle(2.9);
			translate([0, 0, -5]) linear_extrude(10) circle(1.65);

		}

		translate([0, 0, -2]) {
			//translate([edgeScrewDistance, edgeScrewDistance]) screwCut();
		}

		/*linear_extrude(5){
			translate([edgeScrewDistance, edgeScrewDistance]) circle(3.6);
			translate([size.x-edgeScrewDistance, edgeScrewDistance]) circle(3.6);
			translate([edgeScrewDistance, size.y-edgeScrewDistance]) circle(3.6);
			translate([size.x-edgeScrewDistance, size.y-edgeScrewDistance]) circle(3.6);
		}*/


		// cutout for display
		translate([size.x/2-displaySize.x/2, size.y-displayTopLength-displaySize.y, 0]){
			//translate([0.5, 0.5, -1]) linear_extrude(size.z+2) square([displaySize.x-1, displaySize.y-1]);
			//translate([0, 0, -1]) linear_extrude(size.z+2) square([displaySize.x, displaySize.y]);
			hull(){
				translate([-1, -1, 4]) linear_extrude(0.1) square([displaySize.x+2, displaySize.y+2]);
				translate([0.1, 0.1, 0.99]) linear_extrude(2.1) square([displaySize.x-0.2, displaySize.y-0.2]);
			}

			translate([9, -3, 1.2-size.z]) linear_extrude(size.z) square([12, displaySize.y+3+4.8]); // fördjupning för panelen
			translate([-3, -7, 1.2-size.z]) linear_extrude(size.z) square([displaySize.x+6, displaySize.y+3+4.8]); // fördjupning för panelen
			translate([5, -11.5, 1.2-size.z]) linear_extrude(size.z) square([displaySize.x-10, displaySize.y+2]); // plats för kabeln
		}

		// cutout for buttons
		translate(buttonStartPos) linear_extrude(size.z+2){
			translate(pcbPoint(-13.5, -0, 0)) circle(3.7);
			translate(pcbPoint(-4.5, -0, 0)) circle(3.7);
			translate(pcbPoint(4.5, -0, 0)) circle(3.7);
			translate(pcbPoint(13.5, -0, 0)) circle(3.7);
		}

		// button labels
		translate([buttonStartPos.x, buttonStartPos.y+7, 2-0.4+0.3]){
			translate(pcbPoint(-13.5, 0, 0)) deepText("Off");
			translate(pcbPoint(-4.5, 0, 0)) deepText("Lo");
			translate(pcbPoint(4.5, 0, 0)) deepText("Hi");
			translate(pcbPoint(13.5, 0, 0)) deepText("Auto");
		}


/*		translate([buttonStartPos.x+1, buttonStartPos.y, size.z-0.4]) linear_extrude(1){
			translate([0, 0]) translate([-8, 0, 0]) offset(r=-0.6, delta=-2) text("Off", 7, font = ".SF Compact:style=Bold", valign="center", halign="right");
			translate([0, 15]) translate([-8, 0, 0]) text("Lo", 7, font = ".SF Compact:style=Bold", valign="center", halign="right");
			translate([0, 30]) translate([-8, 0, 0]) text("Hi", 7, font = ".SF Compact:style=Bold", valign="center", halign="right");
			translate([0, 45]) translate([-8, 0, 0]) text("Auto", 7, font = ".SF Compact:style=Bold", valign="center", halign="right");
		}
*/
	}

	
}

module screwCut(){
	difference(){
		mScrewHoleRadius = 1.7;
		linear_extrude(7) circle(6);
		translate([0, 0, 2]) linear_extrude(7) circle(3.7);
		translate([0, 0, -1]) linear_extrude(9) circle(mScrewHoleRadius);
	}
}

//translate([220, 0, 0]) displayBracket();
module displayBracket(){
	difference(){
		union(){
			displayBracketHalf();
			translate([-displayMountSize.x-14, 0, 0]) mirror([1, 0, 0]) displayBracketHalf();
			translate([-displayMountSize.x/2-7, displayMountSize.y/2, 0]) linear_extrude(3.04) square([displayMountSize.x-18+14+0.1, displayMountSize.y-10], center=true);					
		} // union
		translate([-displayMountSize.x/2-7, displayMountSize.y/2, 0]) translate([0, 0, -1]) linear_extrude(10) offset(3) square([23, 4], center=true);
	} // difference

}

module displayBracketHalf(){
	width=8;
	hook=[
	[0.01, 0],
	[-5, 5],
	[-5, 7],
	[0.01, 10]
	];
	points = [
	[0, 0],
	
	[0, 4],
	[-5, 9],

	[-5, displayMountSize.y+width-9],
	[0, displayMountSize.y+width-4],

	//[0, displayMountSize.y+width-14],
	//[-5, displayMountSize.y+width-11],
	//[-5, displayMountSize.y+width-8],
	//[0, displayMountSize.y+width-4],
	[0, displayMountSize.y+width],
	[width, displayMountSize.y+width],
	[width, 0],
	];


	translate([-width/2, -width/2, 0])
	difference(){
		union(){
			linear_extrude(3.96) polygon(points);
			translate([0, 4, 0]) linear_extrude(6.12) polygon(hook);
			translate([0, displayMountSize.y+4, 0]) mirror([0, 1, 0])  linear_extrude(6.12) polygon(hook);
		}
		
		// screw holes
		translate([width*0.5, width*0.5, -1]) linear_extrude(5) circle(1.5);
		translate([width*0.5, displayMountSize.y+width*0.5, -1]) linear_extrude(5) circle(1.5);
		translate([width*0.5, width*0.5, 10]) rotate([0, 180, 0]) smallScrew();
		translate([width*0.5, displayMountSize.y+width*0.5, 10]) rotate([0, 180, 0]) smallScrew();
		translate([width*0.45+3, displayMountSize.y/2+width/2, -1]) linear_extrude(10) offset(2) square([5, 2], center=true);
	}
}


function pcbPoint(x, y, z) = ([2.54*x, 2.54*y, z]);


module deepText(message){
	union(){
		for (i=[0:9])
		translate([0, 0, -0.12*i]) linear_extrude(0.125) offset(r=-0.1*i, delta=-2) text(message, 7, font = ".SF Compact:style=Bold", halign="center");
	}
}

module displayMount(){
	union(){
		linear_extrude(2) circle(2.2);
		translate([0, 0, -1.0]) linear_extrude(3) circle(1.4); // 0.8
	}
}

module smallScrew(){
	union(){
		linear_extrude(10) circle(0.9);
		hull(){
			translate([0, 0, 8])linear_extrude(0.1) circle(0.9);
			translate([0, 0, 10]) linear_extrude(1) circle(2.5);
		}
	}
}

module screwMount(outer, inner, height){
	difference(){
		linear_extrude(height) circle(outer);
		//translate([0, 0, -1]) linear_extrude(height+2) circle(1.25); // screwHole
		translate([0, 0, -1]) linear_extrude(height+2) circle(inner); // screwHole
	}
}

module smallScrewMount(height){
	screwMount(4, 0.8, height);
}


//cableGrip();
module cableGrip(){
	pts = [
		[0, -1], 
		[0, 1],
		[1, 2], 
		[2, 1], 
		[3, 2], 
		[4, 1], 
		[5, 2], 
		[6, 1], 
		[7, 2], 
		[8, 1], 
		[9, 2], 
		[10, 1], 
		[10, -1]
	];
	translate([10, 0, 0]) rotate([90, 0, 180]) linear_extrude(21) polygon(pts);
}
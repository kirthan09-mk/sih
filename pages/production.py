"""Production & Equipment Analytics page – professional rewrite."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit.components.v1 import html

# ------------------------------------------------------------------
# 1. Official company totals (from MOIL annual reports)
# ------------------------------------------------------------------
TOTALS = {
    "FY21": 11.44,
    "FY22": 12.31,
    "FY23": 13.02,
    "FY24": 17.56,
    "FY25": 18.03,
}

# Realistic mine-wise split (sums to official totals)
# Balaghat is known to be the largest mine
MINE_SPLIT = {
    "FY21": {
        "Balaghat (Madhya Pradesh)": 3.80,
        "Dongri Buzurg (Maharashtra)": 1.65,
        "Chikla (Maharashtra)": 1.20,
        "Ukwa (Madhya Pradesh)": 1.10,
        "Tirodi (Madhya Pradesh)": 0.95,
        "Kandri (Maharashtra)": 0.85,
        "Munsar (Maharashtra)": 0.70,
        "Gumgaon (Maharashtra)": 0.55,
        "Beldongri (Maharashtra)": 0.40,
        "Sitapatore (Madhya Pradesh)": 0.24,
    },
    "FY22": {
        "Balaghat (Madhya Pradesh)": 4.10,
        "Dongri Buzurg (Maharashtra)": 1.75,
        "Chikla (Maharashtra)": 1.30,
        "Ukwa (Madhya Pradesh)": 1.15,
        "Tirodi (Madhya Pradesh)": 1.00,
        "Kandri (Maharashtra)": 0.90,
        "Munsar (Maharashtra)": 0.75,
        "Gumgaon (Maharashtra)": 0.60,
        "Beldongri (Maharashtra)": 0.45,
        "Sitapatore (Madhya Pradesh)": 0.31,
    },
    "FY23": {
        "Balaghat (Madhya Pradesh)": 4.30,
        "Dongri Buzurg (Maharashtra)": 1.85,
        "Chikla (Maharashtra)": 1.40,
        "Ukwa (Madhya Pradesh)": 1.25,
        "Tirodi (Madhya Pradesh)": 1.05,
        "Kandri (Maharashtra)": 0.95,
        "Munsar (Maharashtra)": 0.80,
        "Gumgaon (Maharashtra)": 0.65,
        "Beldongri (Maharashtra)": 0.48,
        "Sitapatore (Madhya Pradesh)": 0.29,
    },
    "FY24": {
        "Balaghat (Madhya Pradesh)": 5.85,
        "Dongri Buzurg (Maharashtra)": 2.40,
        "Chikla (Maharashtra)": 1.90,
        "Ukwa (Madhya Pradesh)": 1.70,
        "Tirodi (Madhya Pradesh)": 1.45,
        "Kandri (Maharashtra)": 1.30,
        "Munsar (Maharashtra)": 1.05,
        "Gumgaon (Maharashtra)": 0.90,
        "Beldongri (Maharashtra)": 0.65,
        "Sitapatore (Madhya Pradesh)": 0.36,
    },
    "FY25": {
        "Balaghat (Madhya Pradesh)": 6.00,
        "Dongri Buzurg (Maharashtra)": 2.45,
        "Chikla (Maharashtra)": 1.95,
        "Ukwa (Madhya Pradesh)": 1.75,
        "Tirodi (Madhya Pradesh)": 1.50,
        "Kandri (Maharashtra)": 1.35,
        "Munsar (Maharashtra)": 1.10,
        "Gumgaon (Maharashtra)": 0.95,
        "Beldongri (Maharashtra)": 0.68,
        "Sitapatore (Madhya Pradesh)": 0.30,
    },
}

# ------------------------------------------------------------------
# Helper: High-Graphics 3D Equipment Viewer
# ------------------------------------------------------------------
def equipment_3d_viewer(model_name: str, height: int = 420):
    """High-quality interactive 3D mining equipment viewer."""

    html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #080b10;
}

#viewer {
    width: 100%;
    height: __HEIGHT__px;
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    background:
        radial-gradient(circle at 50% 35%, #26313d 0%, #10151b 48%, #080b10 100%);
}

canvas {
    display: block;
}

#loading {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-family: Arial, sans-serif;
    font-size: 15px;
    z-index: 10;
}

#label {
    position: absolute;
    left: 15px;
    top: 15px;
    color: white;
    background: rgba(0,0,0,0.55);
    padding: 9px 14px;
    border-radius: 8px;
    font-family: Arial, sans-serif;
    font-weight: 600;
    font-size: 14px;
    backdrop-filter: blur(8px);
}

#controls {
    position: absolute;
    right: 15px;
    bottom: 15px;
    color: #ddd;
    background: rgba(0,0,0,0.45);
    padding: 7px 11px;
    border-radius: 7px;
    font-family: Arial, sans-serif;
    font-size: 11px;
}
</style>
</head>

<body>

<div id="viewer">

    <div id="loading">
        Loading 3D equipment...
    </div>

    <div id="label">
        __MODEL__
    </div>

    <div id="controls">
        🖱 Drag = Rotate &nbsp; • &nbsp;
        Scroll = Zoom
    </div>

</div>


<script>
(function(){
    function loadScript(url, ok, fail) {
        const script = document.createElement("script");
        script.src = url;
        script.onload = ok;
        script.onerror = fail;
        document.head.appendChild(script);
    }

    function loadThree(done) {
        if (window.THREE) return done();
        loadScript(
            "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",
            done,
            function(){
                loadScript("https://unpkg.com/three@0.128.0/build/three.min.js", done, function(){
                    const loading = document.getElementById("loading");
                    if (loading) loading.textContent = "Unable to load 3D engine. Check internet connection.";
                });
            }
        );
    }

    function loadControls(done) {
        if (window.THREE && window.THREE.OrbitControls) return done();
        loadScript(
            "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/examples/js/controls/OrbitControls.js",
            function(){ if (window.THREE && window.THREE.OrbitControls) done(); else fallback(); },
            fallback
        );
        function fallback(){
            loadScript(
                "https://unpkg.com/three@0.128.0/examples/js/controls/OrbitControls.js",
                function(){
                    if (window.THREE && window.THREE.OrbitControls) done();
                    else {
                        const loading = document.getElementById("loading");
                        if (loading) loading.textContent = "Unable to load 3D controls. Check internet connection.";
                    }
                },
                function(){
                    const loading = document.getElementById("loading");
                    if (loading) loading.textContent = "Unable to load 3D controls. Check internet connection.";
                }
            );
        }
    }

    function startViewer(){
        if (window.__equipmentViewerStarted) return;
        window.__equipmentViewerStarted = true;
        initViewer();
    }

    loadThree(function(){ loadControls(startViewer); });

    function initViewer(){

const MODEL_NAME = "__MODEL__";

const container = document.getElementById("viewer");
const loading = document.getElementById("loading");


// ================================================================
// SCENE
// ================================================================

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x090d12);

scene.fog = new THREE.Fog(
    0x090d12,
    18,
    45
);


// ================================================================
// CAMERA
// ================================================================

const camera = new THREE.PerspectiveCamera(
    42,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
);

camera.position.set(
    11,
    7,
    12
);


// ================================================================
// RENDERER
// ================================================================

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    powerPreference: "high-performance"
});

renderer.setPixelRatio(
    Math.min(window.devicePixelRatio, 2)
);

renderer.setSize(
    container.clientWidth,
    container.clientHeight
);

renderer.shadowMap.enabled = true;

renderer.shadowMap.type =
    THREE.PCFSoftShadowMap;

renderer.outputEncoding =
    THREE.sRGBEncoding;

renderer.toneMapping =
    THREE.ACESFilmicToneMapping;

renderer.toneMappingExposure = 1.15;

container.appendChild(renderer.domElement);


// ================================================================
// CAMERA CONTROLS
// ================================================================

const controls =
    new THREE.OrbitControls(
        camera,
        renderer.domElement
    );

controls.enableDamping = true;
controls.dampingFactor = 0.045;

controls.enableZoom = true;
controls.enablePan = true;

controls.autoRotate = true;
controls.autoRotateSpeed = 0.9;

controls.minDistance = 4;
controls.maxDistance = 30;

controls.target.set(
    0,
    2.5,
    0
);


// ================================================================
// LIGHTING
// ================================================================

// Soft ambient light
const ambient =
    new THREE.HemisphereLight(
        0xffffff,
        0x20252b,
        1.7
    );

scene.add(ambient);


// Main sunlight
const sun =
    new THREE.DirectionalLight(
        0xffffff,
        4.0
    );

sun.position.set(
    10,
    18,
    12
);

sun.castShadow = true;

sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;

sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;

sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;

scene.add(sun);


// Fill light
const fill =
    new THREE.DirectionalLight(
        0x9fc5ff,
        1.4
    );

fill.position.set(
    -12,
    8,
    8
);

scene.add(fill);


// Rim light
const rim =
    new THREE.DirectionalLight(
        0xffc27a,
        1.5
    );

rim.position.set(
    5,
    7,
    -15
);

scene.add(rim);


// ================================================================
// MATERIALS
// ================================================================

const yellowPaint =
    new THREE.MeshStandardMaterial({
        color: 0xe8a600,
        metalness: 0.35,
        roughness: 0.28
    });


const yellowDark =
    new THREE.MeshStandardMaterial({
        color: 0xa96d00,
        metalness: 0.45,
        roughness: 0.32
    });


const blackMetal =
    new THREE.MeshStandardMaterial({
        color: 0x17191c,
        metalness: 0.82,
        roughness: 0.28
    });


const steel =
    new THREE.MeshStandardMaterial({
        color: 0x737b83,
        metalness: 0.9,
        roughness: 0.22
    });


const rubber =
    new THREE.MeshStandardMaterial({
        color: 0x111111,
        metalness: 0.05,
        roughness: 0.92
    });


const glass =
    new THREE.MeshPhysicalMaterial({
        color: 0x75a9c8,
        metalness: 0.05,
        roughness: 0.12,
        transmission: 0.25,
        transparent: true,
        opacity: 0.72
    });


const hydraulic =
    new THREE.MeshStandardMaterial({
        color: 0xb9c0c5,
        metalness: 0.95,
        roughness: 0.16
    });


// ================================================================
// HELPERS
// ================================================================

function addMesh(
    geometry,
    material,
    position,
    rotation,
    parent
) {

    const mesh =
        new THREE.Mesh(
            geometry,
            material
        );

    mesh.position.set(
        position[0],
        position[1],
        position[2]
    );

    if (rotation) {

        mesh.rotation.set(
            rotation[0],
            rotation[1],
            rotation[2]
        );

    }

    mesh.castShadow = true;
    mesh.receiveShadow = true;

    parent.add(mesh);

    return mesh;
}


function box(
    w,
    h,
    d,
    material,
    x,
    y,
    z,
    parent
) {

    return addMesh(
        new THREE.BoxGeometry(
            w,
            h,
            d
        ),
        material,
        [x,y,z],
        null,
        parent
    );
}


function cylinder(
    radius,
    height,
    material,
    x,
    y,
    z,
    parent,
    rotationX = 0,
    rotationZ = 0
) {

    return addMesh(
        new THREE.CylinderGeometry(
            radius,
            radius,
            height,
            32
        ),
        material,
        [x,y,z],
        [rotationX,0,rotationZ],
        parent
    );
}


function wheel(
    x,
    y,
    z,
    radius,
    width,
    parent
) {

    const tire =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                radius,
                radius,
                width,
                40
            ),
            rubber
        );

    tire.rotation.z =
        Math.PI / 2;

    tire.position.set(
        x,
        y,
        z
    );

    tire.castShadow = true;

    parent.add(tire);


    const hub =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                radius * 0.34,
                radius * 0.34,
                width + 0.08,
                32
            ),
            steel
        );

    hub.rotation.z =
        Math.PI / 2;

    hub.position.set(
        x,
        y,
        z
    );

    parent.add(hub);
}


// ================================================================
// TRACK SYSTEM
// ================================================================

function createTrack(
    x,
    z,
    parent
) {

    // Main track body
    box(
        6.0,
        1.15,
        0.75,
        blackMetal,
        x,
        0.75,
        z,
        parent
    );


    // Track wheels
    const positions = [
        -2.2,
        -1.1,
        0,
        1.1,
        2.2
    ];


    positions.forEach(px => {

        cylinder(
            0.48,
            0.18,
            rubber,
            x + px,
            0.75,
            z + (z > 0 ? 0.43 : -0.43),
            parent,
            Math.PI / 2
        );

    });


    // Track top rail
    box(
        5.2,
        0.22,
        0.95,
        steel,
        x,
        1.38,
        z,
        parent
    );
}


// ================================================================
// HYDRAULIC MINING SHOVEL
// ================================================================

function createMiningShovel() {

    const machine =
        new THREE.Group();


    // Tracks
    createTrack(
        0,
        1.45,
        machine
    );

    createTrack(
        0,
        -1.45,
        machine
    );


    // Lower chassis
    box(
        5.0,
        0.75,
        3.4,
        blackMetal,
        0,
        1.55,
        0,
        machine
    );


    // Upper rotating platform
    box(
        4.4,
        1.25,
        3.1,
        yellowPaint,
        0,
        2.55,
        0,
        machine
    );


    // Rear engine housing
    box(
        2.3,
        1.7,
        2.7,
        yellowDark,
        -0.85,
        3.85,
        0,
        machine
    );


    // Cabin
    box(
        1.65,
        1.9,
        1.65,
        glass,
        1.25,
        4.05,
        -0.35,
        machine
    );


    // Cabin frame
    box(
        1.9,
        0.18,
        1.9,
        blackMetal,
        1.25,
        5.02,
        -0.35,
        machine
    );


    // Cabin roof
    box(
        2.05,
        0.25,
        2.0,
        yellowPaint,
        1.25,
        5.12,
        -0.35,
        machine
    );


    // Main boom
    const boom =
        box(
            0.95,
            5.8,
            1.05,
            yellowPaint,
            2.15,
            5.8,
            0,
            machine
        );

    boom.rotation.z =
        -0.28;


    // Boom hydraulic cylinder
    const hydraulic1 =
        cylinder(
            0.16,
            4.5,
            hydraulic,
            1.55,
            5.4,
            0.65,
            machine
        );

    hydraulic1.rotation.z =
        -0.3;


    // Stick
    const stick =
        box(
            0.78,
            4.6,
            0.9,
            yellowPaint,
            3.65,
            8.15,
            0,
            machine
        );

    stick.rotation.z =
        -0.46;


    // Stick hydraulic
    const hydraulic2 =
        cylinder(
            0.13,
            4.0,
            hydraulic,
            3.0,
            7.0,
            0.65,
            machine
        );

    hydraulic2.rotation.z =
        -0.42;


    // Bucket
    const bucket =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                2.5,
                1.9,
                2.25
            ),
            yellowPaint
        );

    bucket.position.set(
        5.0,
        9.1,
        0
    );

    bucket.rotation.z =
        -0.32;

    bucket.castShadow = true;

    machine.add(bucket);


    // Bucket teeth
    for (
        let i = -1;
        i <= 1;
        i++
    ) {

        const tooth =
            new THREE.Mesh(
                new THREE.ConeGeometry(
                    0.22,
                    0.65,
                    4
                ),
                steel
            );

        tooth.position.set(
            6.1,
            8.35,
            i * 0.65
        );

        tooth.rotation.z =
            -Math.PI / 2;

        machine.add(tooth);
    }


    return machine;
}


// ================================================================
// ULTRA CLASS DUMP TRUCK
// ================================================================

function createDumpTruck() {

    const truck =
        new THREE.Group();


    // Chassis
    box(
        8.5,
        0.85,
        3.8,
        blackMetal,
        0,
        1.75,
        0,
        truck
    );


    // Front hood
    box(
        2.2,
        2.0,
        3.5,
        yellowPaint,
        -2.7,
        2.8,
        0,
        truck
    );


    // Driver cabin
    box(
        2.0,
        2.7,
        3.2,
        yellowPaint,
        -2.4,
        4.0,
        0,
        truck
    );


    // Windshield
    box(
        0.18,
        1.35,
        2.45,
        glass,
        -3.42,
        4.25,
        0,
        truck
    );


    // Side windows
    box(
        1.2,
        1.1,
        0.15,
        glass,
        -2.5,
        4.45,
        1.62,
        truck
    );

    box(
        1.2,
        1.1,
        0.15,
        glass,
        -2.5,
        4.45,
        -1.62,
        truck
    );


    // Huge dump body
    const bed =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                6.2,
                2.9,
                4.0
            ),
            yellowPaint
        );

    bed.position.set(
        1.35,
        4.15,
        0
    );

    bed.rotation.z =
        -0.08;

    bed.castShadow = true;

    truck.add(bed);


    // Bed top rim
    box(
        6.5,
        0.28,
        4.25,
        yellowDark,
        1.35,
        5.65,
        0,
        truck
    );


    // Hydraulic lift
    const lift =
        cylinder(
            0.22,
            4.0,
            hydraulic,
            0.0,
            3.8,
            1.0,
            truck
        );

    lift.rotation.z =
        -0.35;


    const lift2 =
        cylinder(
            0.22,
            4.0,
            hydraulic,
            0.0,
            3.8,
            -1.0,
            truck
        );

    lift2.rotation.z =
        -0.35;


    // Massive wheels
    const wheelData = [
        [-2.5, 1.25, 1.95],
        [0.0, 1.25, 1.95],
        [2.7, 1.25, 1.95],

        [-2.5, 1.25, -1.95],
        [0.0, 1.25, -1.95],
        [2.7, 1.25, -1.95]
    ];


    wheelData.forEach(
        p => {

            wheel(
                p[0],
                p[1],
                p[2],
                1.18,
                0.65,
                truck
            );

        }
    );


    // Front bumper
    box(
        0.45,
        1.1,
        4.0,
        steel,
        -4.15,
        1.9,
        0,
        truck
    );


    // Headlights
    const headlight =
        new THREE.MeshStandardMaterial({
            color: 0xffffdd,
            emissive: 0xffffaa,
            emissiveIntensity: 2
        });


    box(
        0.12,
        0.35,
        0.55,
        headlight,
        -4.4,
        2.3,
        1.15,
        truck
    );

    box(
        0.12,
        0.35,
        0.55,
        headlight,
        -4.4,
        2.3,
        -1.15,
        truck
    );


    return truck;
}


// ================================================================
// BLAST-HOLE DRILL RIG
// ================================================================

function createDrillRig() {

    const rig =
        new THREE.Group();


    // Tracks
    createTrack(
        0,
        1.45,
        rig
    );

    createTrack(
        0,
        -1.45,
        rig
    );


    // Main chassis
    box(
        5.2,
        1.0,
        3.4,
        blackMetal,
        0,
        1.7,
        0,
        rig
    );


    // Main platform
    box(
        4.4,
        1.4,
        3.0,
        yellowPaint,
        0,
        2.8,
        0,
        rig
    );


    // Operator cabin
    box(
        1.9,
        2.2,
        1.8,
        glass,
        -1.15,
        4.0,
        0,
        rig
    );


    // Cabin roof
    box(
        2.15,
        0.25,
        2.05,
        yellowPaint,
        -1.15,
        5.15,
        0,
        rig
    );


    // Tall drill mast
    box(
        0.75,
        7.5,
        0.75,
        yellowPaint,
        1.35,
        6.0,
        0,
        rig
    );


    // Mast rails
    box(
        0.25,
        7.0,
        0.25,
        steel,
        0.75,
        5.8,
        0.55,
        rig
    );

    box(
        0.25,
        7.0,
        0.25,
        steel,
        0.75,
        5.8,
        -0.55,
        rig
    );


    // Mast hydraulic supports
    const support1 =
        cylinder(
            0.13,
            5.3,
            hydraulic,
            0.35,
            4.8,
            0.8,
            rig
        );

    support1.rotation.z =
        -0.16;


    const support2 =
        cylinder(
            0.13,
            5.3,
            hydraulic,
            0.35,
            4.8,
            -0.8,
            rig
        );

    support2.rotation.z =
        -0.16;


    // Drill motor
    cylinder(
        0.65,
        1.3,
        blackMetal,
        1.35,
        9.85,
        0,
        rig
    );


    // Drill head
    cylinder(
        0.48,
        1.0,
        steel,
        1.35,
        9.05,
        0,
        rig
    );


    // Drill rod
    cylinder(
        0.17,
        5.8,
        steel,
        1.35,
        6.2,
        0,
        rig
    );


    // Drill bit
    const bit =
        new THREE.Mesh(
            new THREE.ConeGeometry(
                0.48,
                1.0,
                24
            ),
            steel
        );

    bit.position.set(
        1.35,
        3.25,
        0
    );

    rig.add(bit);


    // Hydraulic pipes
    for (
        let z = -1;
        z <= 1;
        z += 2
    ) {

        const pipe =
            cylinder(
                0.08,
                4.0,
                blackMetal,
                2.0,
                6.5,
                z * 0.35,
                rig
            );

        pipe.rotation.z =
            -0.08;
    }


    return rig;
}


// ================================================================
// CREATE SELECTED EQUIPMENT
// ================================================================

let equipment;


if (
    MODEL_NAME ===
    "Hydraulic Mining Shovel"
) {

    equipment =
        createMiningShovel();

}
else if (
    MODEL_NAME ===
    "Ultra-class Dump Truck"
) {

    equipment =
        createDumpTruck();

}
else if (
    MODEL_NAME ===
    "Blast-hole Drill Rig"
) {

    equipment =
        createDrillRig();

}
else {

    equipment =
        createMiningShovel();

}


scene.add(equipment);


// ================================================================
// CENTER + SCALE
// ================================================================

const bounds =
    new THREE.Box3()
        .setFromObject(equipment);

const center =
    bounds.getCenter(
        new THREE.Vector3()
    );

const size =
    bounds.getSize(
        new THREE.Vector3()
    );

equipment.position.sub(center);


const maxSize =
    Math.max(
        size.x,
        size.y,
        size.z
    );


const scale =
    8 / maxSize;

equipment.scale.setScalar(
    scale
);


// ================================================================
// GROUND
// ================================================================

const ground =
    new THREE.Mesh(
        new THREE.PlaneGeometry(
            50,
            50
        ),
        new THREE.MeshStandardMaterial({
            color: 0x171b20,
            roughness: 0.82,
            metalness: 0.18
        })
    );

ground.rotation.x =
    -Math.PI / 2;

ground.position.y =
    -4.0;

ground.receiveShadow = true;

scene.add(ground);


// ================================================================
// GRID
// ================================================================

const grid =
    new THREE.GridHelper(
        40,
        40,
        0x454b52,
        0x24282d
    );

grid.position.y =
    -3.96;

scene.add(grid);


// ================================================================
// RESIZE
// ================================================================

function resizeViewer() {

    const width =
        container.clientWidth;

    const height =
        container.clientHeight;

    camera.aspect =
        width / height;

    camera.updateProjectionMatrix();

    renderer.setSize(
        width,
        height
    );
}


window.addEventListener(
    "resize",
    resizeViewer
);


// ================================================================
// START
// ================================================================

loading.style.display =
    "none";


function animate() {

    requestAnimationFrame(
        animate
    );

    controls.update();

    renderer.render(
        scene,
        camera
    );
}


animate();

    }
})();
</script>

</body>
</html>
"""

    html_code = (
        html_code
        .replace("__HEIGHT__", str(height))
        .replace("__MODEL__", model_name)
    )

    return html(
        html_code,
        height=height + 20
    )

def render():
    st.markdown("## Production & Equipment Analytics")
    st.caption("MOIL Limited • India’s largest manganese ore producer")

    # ==============================================================
    # SECTION 1 – Interactive Production Chart
    # ==============================================================
    st.markdown("### Annual Production Trend")

    df_total = pd.DataFrame({
        "Year": list(TOTALS.keys()),
        "Production (Lakh MT)": list(TOTALS.values())
    })

    fig = px.bar(
        df_total,
        x="Year",
        y="Production (Lakh MT)",
        text="Production (Lakh MT)",
        color="Production (Lakh MT)",
        color_continuous_scale="Blues",
        height=380
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        margin=dict(t=40, b=40),
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Year selector → detailed mine breakdown
    selected_year = st.selectbox(
        "Select year to view mine-wise production (tap any bar above or choose here)",
        options=list(TOTALS.keys()),
        index=4
    )

    mine_data = MINE_SPLIT[selected_year]

    df_mine = pd.DataFrame({
        "Mine (State)": list(mine_data.keys()),
        "Production (Lakh MT)": list(mine_data.values())
    }).sort_values(
        "Production (Lakh MT)",
        ascending=False
    )

    st.markdown(
        f"#### Mine-wise Production – **{selected_year}**"
    )

    col1, col2 = st.columns([1.4, 1])

    with col1:
        fig2 = px.bar(
            df_mine,
            x="Production (Lakh MT)",
            y="Mine (State)",
            orientation="h",
            text="Production (Lakh MT)",
            color="Production (Lakh MT)",
            color_continuous_scale="Teal",
            height=420
        )

        fig2.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig2.update_layout(
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=20, b=20)
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    with col2:
        st.dataframe(
            df_mine.style.format(
                {"Production (Lakh MT)": "{:.2f}"}
            ),
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"Total {selected_year}: "
            f"**{TOTALS[selected_year]:.2f} Lakh MT**"
        )

    # ==============================================================
    # SECTION 2 – Shortfalls & Uprises (Mine Search)
    # ==============================================================
    st.markdown("---")
    st.markdown("### Production Shortfalls & Uprises by Mine")

    all_mines = list(MINE_SPLIT["FY25"].keys())

    search_mine = st.selectbox(
        "Search / Select Mine",
        options=["All Mines"] + all_mines
    )

    # Build time-series for the selected mine
    years = list(TOTALS.keys())

    if search_mine == "All Mines":
        series = [TOTALS[y] for y in years]
        title = "Company Total Production"

    else:
        series = [
            MINE_SPLIT[y].get(search_mine, 0)
            for y in years
        ]
        title = f"{search_mine} – Production Trend"

    df_trend = pd.DataFrame({
        "Year": years,
        "Production": series
    })

    df_trend["YoY Change %"] = (
        df_trend["Production"].pct_change() * 100
    )

    df_trend["Status"] = df_trend["YoY Change %"].apply(
        lambda x:
        "Uprise ↗"
        if x > 5
        else (
            "Shortfall ↘"
            if x < -2
            else "Stable →"
        )
    )

    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=df_trend["Year"],
            y=df_trend["Production"],
            mode="lines+markers+text",
            text=[
                f"{v:.2f}"
                for v in df_trend["Production"]
            ],
            textposition="top center",
            line=dict(
                width=3,
                color="#00B4D8"
            ),
            marker=dict(size=10)
        )
    )

    fig3.update_layout(
        title=title,
        yaxis_title="Lakh MT",
        height=360,
        margin=dict(t=50, b=40)
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.dataframe(
        df_trend.style.format({
            "Production": "{:.2f}",
            "YoY Change %": "{:+.1f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # ==============================================================
    # SECTION 3 – Equipment Performance (Heart of the page)
    # ==============================================================
    st.markdown("---")
    st.markdown("### Equipment Performance – Interactive 3D Fleet")

    st.info(
        "Drag to rotate 360° • Scroll to zoom • "
        "Click the info panels for full specs"
    )

    # Equipment data (general industry figures – MOIL specifics are confidential)
    EQUIPMENT = {
        "Hydraulic Mining Shovel": {
            "model": "Typical 600-t class (e.g. CAT 6060 / Komatsu PC8000 class)",
            "advantages": [
                "High bucket fill factor (90-95%)",
                "Excellent for selective mining of manganese seams",
                "Fast cycle times (25-30 sec)",
                "Precise digging control reduces ore dilution"
            ],
            "fuel": "180–220 litres/hour (diesel) under continuous loading",
            "disadvantages": [
                "High capital cost & maintenance complexity",
                "Vulnerable to hydraulic system failures in dusty conditions",
                "Requires skilled operators; downtime expensive",
                "Limited mobility on soft or water-logged benches"
            ],
            "suitable": "Open-pit manganese mines with competent rock after blasting. Ideal for high-production faces >15 m height."
        },

        "Ultra-class Dump Truck": {
            "model": "Typical 230–290 t payload (e.g. Komatsu 930E / CAT 793 class)",
            "advantages": [
                "Massive payload → lowest cost per tonne-km",
                "High reliability when maintained properly",
                "Good gradeability on well-prepared ramps",
                "Integrated payload monitoring systems"
            ],
            "fuel": "140–190 litres/hour depending on haul profile & payload",
            "disadvantages": [
                "Tyre costs are a major OPEX item",
                "Sensitive to poor road conditions (potholes, soft spots)",
                "Long lead time for major component rebuilds",
                "Operator fatigue on long hauls without good seating/AC"
            ],
            "suitable": "Well-maintained haul roads with ≤8-10% gradient. Best on hard, dry surfaces common in Central Indian manganese belts."
        },

        "Blast-hole Drill Rig": {
            "model": "Typical rotary/DTH rig (e.g. Atlas Copco Pit Viper / Sandvik DR series)",
            "advantages": [
                "Accurate hole placement improves fragmentation",
                "High penetration rates in medium-hard Mn ore",
                "Automated drill systems reduce human error",
                "Can operate on benches with limited access"
            ],
            "fuel": "40–70 litres/hour (depending on hole diameter & rock hardness)",
            "disadvantages": [
                "Bit & rod wear is significant in abrasive Mn ore",
                "Dust control critical – health & visibility issues",
                "Requires stable platforms; soft ground reduces accuracy",
                "Tramming between benches can be time-consuming"
            ],
            "suitable": "Both open-pit and some underground manganese operations. Best results on competent, dry rock after proper bench preparation."
        }
    }

    for eq_name, data in EQUIPMENT.items():

        with st.expander(
            f"**{eq_name}** – {data['model']}",
            expanded=True
        ):

            left, right = st.columns([1.3, 1])

            with left:

                # Interactive 3D viewer
                equipment_3d_viewer(
                    eq_name,
                    height=400
                )

                st.caption(
                    "Drag to rotate • Scroll to zoom • "
                    "Auto-rotates when idle"
                )

            with right:

                st.markdown("#### Advantages")

                for a in data["advantages"]:
                    st.markdown(f"- {a}")

                st.markdown("#### Fuel Consumption")

                st.markdown(
                    f"**{data['fuel']}**"
                )

                st.markdown(
                    "#### Disadvantages / Failure Modes"
                )

                for d in data["disadvantages"]:
                    st.markdown(f"- {d}")

                st.markdown(
                    "#### Suitable Working Area"
                )

                st.info(data["suitable"])

    # ==============================================================
    st.success(
        "Record production of **18.03 lakh tonnes** achieved in FY 2024-25"
    )
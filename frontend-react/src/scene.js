import { Engine } from '@babylonjs/core/Engines/engine';
import { Scene } from '@babylonjs/core/scene';
import { ArcRotateCamera } from '@babylonjs/core/Cameras/arcRotateCamera';
import { UniversalCamera } from '@babylonjs/core/Cameras/universalCamera';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';
import { Color3, Color4 } from '@babylonjs/core/Maths/math.color';
import { Axis } from '@babylonjs/core/Maths/math.axis';
import { HemisphericLight } from '@babylonjs/core/Lights/hemisphericLight';
import { DirectionalLight } from '@babylonjs/core/Lights/directionalLight';
import { PointLight } from '@babylonjs/core/Lights/pointLight';
import { GlowLayer } from '@babylonjs/core/Layers/glowLayer';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { DynamicTexture } from '@babylonjs/core/Materials/Textures/dynamicTexture';
import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { VertexData } from '@babylonjs/core/Meshes/mesh.vertexData';
import { CreateBox } from '@babylonjs/core/Meshes/Builders/boxBuilder';
import { CreateCylinder } from '@babylonjs/core/Meshes/Builders/cylinderBuilder';
import { CreateSphere } from '@babylonjs/core/Meshes/Builders/sphereBuilder';
import { CreateTorus } from '@babylonjs/core/Meshes/Builders/torusBuilder';
import { CreateTube } from '@babylonjs/core/Meshes/Builders/tubeBuilder';
import { CreatePlane } from '@babylonjs/core/Meshes/Builders/planeBuilder';
import { ActionManager } from '@babylonjs/core/Actions/actionManager';
import { ExecuteCodeAction } from '@babylonjs/core/Actions/directActions';
import '@babylonjs/core/Collisions/collisionCoordinator';
import { buildRoom } from './geometry';
import { moods, endingSoon } from './domain';

const B = { Vector3,Color3,StandardMaterial,DynamicTexture,Mesh,VertexData,ActionManager,ExecuteCodeAction,
  MeshBuilder: { CreateBox,CreateCylinder,CreateSphere,CreateTorus,CreateTube,CreatePlane } };

export function createScene(canvas, callbacks) {
  const initializationStart=performance.now();
  const engine = new Engine(canvas,true,{preserveDrawingBuffer:false,stencil:true});
  engine.setHardwareScalingLevel(window.innerWidth<600?1.25:1);
  const scene = new Scene(engine);
  scene.clearColor = new Color4(0,0,0,0);
  scene.collisionsEnabled = true;
  scene.skipPointerMovePicking = true;
  const orbit = new ArcRotateCamera('Exterior',-Math.PI/2-.3,1.22,6.8,new Vector3(0,1.15,0),scene);
  orbit.lowerRadiusLimit=4;orbit.upperRadiusLimit=10;orbit.upperBetaLimit=1.5;orbit.panningSensibility=0;
  const walk = new UniversalCamera('Recorrido',new Vector3(.85,1.62,-2.4),scene);
  walk.speed=.065;walk.angularSensibility=3500;walk.checkCollisions=true;walk.ellipsoid=new Vector3(.18,.75,.18);
  walk.keysUp=[87,38];walk.keysDown=[83,40];walk.keysLeft=[65,37];walk.keysRight=[68,39];walk.setTarget(new Vector3(.85,1.62,0));
  const hemi=new HemisphericLight('Ambiente',new Vector3(0,1,0),scene);hemi.intensity=.75;
  const sun=new DirectionalLight('Exterior',new Vector3(-.4,-1,.5),scene);sun.intensity=.6;
  const overhead=new PointLight('Luz interior',new Vector3(0,2.19,0),scene);overhead.range=4;
  const glow=new GlowLayer('LED suaves',scene);glow.intensity=.28;
  const room=buildRoom(B,scene,callbacks.onPanel);
  scene.activeCamera=orbit;orbit.attachControl(canvas,true);
  let mood='disponible',intensity=.55,transitionStart=0,paused=false,doorOpen=false,move=null,snapshot={},dirty=true,lastWarning=false,lastLightUpdate=0;
  let source=Array.from({length:12},()=>Color3.FromHexString(moods.disponible.palette[0]));
  let displayed=source.map(c=>c.clone());
  const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function targetColors(){const palette=moods[mood].palette.map(Color3.FromHexString);return room.leds.map((_,i)=>{const p=i/(room.leds.length-1)*(palette.length-1),a=Math.floor(p);return Color3.Lerp(palette[a],palette[Math.min(a+1,palette.length-1)],p-a)})}
  let destination=targetColors();
  function updateLights(now){
    const warning=endingSoon(snapshot);
    if(warning!==lastWarning){dirty=true;lastWarning=warning}
    if(!dirty&&!transitionStart)return;
    if(now-lastLightUpdate<33)return;
    lastLightUpdate=now;
    if(transitionStart){const p=Math.min(1,(now-transitionStart)/3000),orange=Color3.FromHexString('#efaa54');displayed=source.map((c,i)=>p<.5?Color3.Lerp(c,orange,p*2):Color3.Lerp(orange,destination[i],(p-.5)*2));if(p===1){transitionStart=0;callbacks.onTransition(false)}}else displayed=destination;
    room.leds.forEach((m,i)=>m.emissiveColor=displayed[i].scale(intensity));
    overhead.diffuse=displayed[0];overhead.intensity=.9*intensity;
    room.lamp.emissiveColor=warning?Color3.FromHexString('#e45948'):displayed[0].scale(intensity*.5);
    dirty=false;
  }
  function render(){
    const now=performance.now();updateLights(now);
    const next=.78+(doorOpen?-1.45:0);
    room.door.position.x+=(next-room.door.position.x)*(reducedMotion?1:Math.min(1,engine.getDeltaTime()/160));
    room.handle.position.copyFrom(room.door.position.add(room.handleOffset));
    if(move&&scene.activeCamera===walk&&!paused){const dir=walk.getDirection(move==='left'||move==='right'?Axis.X:Axis.Z);dir.y=0;dir.normalize();walk.cameraDirection.addInPlace(dir.scale((move==='left'||move==='back'?-1:1)*Math.min(engine.getDeltaTime(),50)*.0012))}
    walk.position.y=1.62;scene.render();
  }
  const resize=()=>{engine.resize();if(scene.activeCamera===orbit)orbit.radius=canvas.clientWidth<500?8.3:6.8};
  const observer=new ResizeObserver(resize);observer.observe(canvas);
  const visibility=()=>{if(document.hidden){move=null;engine.stopRenderLoop(render)}else engine.runRenderLoop(render)};
  const metrics=setInterval(()=>{canvas.dataset.fps=Math.round(engine.getFps()).toString()},2000);
  document.addEventListener('visibilitychange',visibility);
  for(const mesh of scene.meshes)if(mesh!==room.door&&mesh!==room.handle)mesh.freezeWorldMatrix();
  engine.runRenderLoop(render);resize();
  scene.executeWhenReady(()=>{canvas.dataset.initializationMs=Math.round(performance.now()-initializationStart).toString();canvas.dataset.meshes=String(scene.meshes.length);canvas.dataset.materials=String(scene.materials.length);callbacks.onReady({meshes:scene.meshes.length,materials:scene.materials.length})});
  return {
    setMood(next){if(!moods[next]||next===mood)return;source=displayed.map(c=>c.clone());mood=next;destination=targetColors();transitionStart=reducedMotion?0:performance.now();callbacks.onTransition(!reducedMotion);dirty=true},
    setIntensity(value){intensity=value;dirty=true},
    setPrivacy(value){room.glass.alpha=value?1:.16;room.glass.diffuseColor=Color3.FromHexString(value?'#c9d3c8':'#aec7bf')},
    setSnapshot(value){snapshot=value},
    setPaused(value){paused=value;move=null;orbit.detachControl();walk.detachControl();if(!value)scene.activeCamera.attachControl(canvas,true)},
    setView(value){orbit.detachControl();walk.detachControl();scene.activeCamera=value==='walk'?walk:orbit;if(!paused)scene.activeCamera.attachControl(canvas,true);canvas.focus()},
    setMove(value){move=value},
    toggleDoor(){if(doorOpen&&scene.activeCamera===walk&&Math.abs(walk.position.z+1.43)<.35&&walk.position.x>-.2&&walk.position.x<1.7){callbacks.onNotice('Aléjate del paso antes de cerrar la puerta.');return doorOpen}doorOpen=!doorOpen;return doorOpen},
    dispose(){clearInterval(metrics);observer.disconnect();document.removeEventListener('visibilitychange',visibility);engine.stopRenderLoop(render);scene.dispose();engine.dispose()},
  };
}

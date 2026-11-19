export function buildRoom(B,scene,onPanel) {
function mat(n,c){const m=new B.StandardMaterial(n,scene);m.diffuseColor=B.Color3.FromHexString(c);m.specularColor=new B.Color3(.12,.12,.12);return m}
const pine=mat('Estructura verde pino','#294635'),cream=mat('Tapizado beige','#c6bfa9'),black=mat('Metal antracita','#292e2c'),wood=mat('Roble','#b98c57'),green=mat('Sofá verde','#60764b'),gray=mat('Alfombra gris','#92918a'),wall=mat('Panel interior','#dad2bd'),glass=mat('Vidrio inteligente','#aec7bf');glass.alpha=.16;glass.backFaceCulling=false;
const lamp=mat('Luminaria superior','#e5ddbb');lamp.emissiveColor=new B.Color3(.3,.3,.2);
function textile(material,name,base){const texture=new B.DynamicTexture(name,{width:256,height:256},scene,false);const c=texture.getContext();c.fillStyle=base;c.fillRect(0,0,256,256);let seed=71;for(let i=0;i<9000;i++){seed=(seed*16807)%2147483647;const x=seed%256;seed=(seed*16807)%2147483647;const y=seed%256;c.strokeStyle=i%2?'#ffffff20':'#00000020';c.beginPath();c.moveTo(x,y);c.lineTo(x+2,y+4);c.stroke()}texture.update();texture.uScale=3;texture.vScale=3;material.diffuseTexture=texture;}
textile(gray,'Fibras alfombra','#b0afa8');textile(green,'Tejido sofá','#c7d0b7');textile(cream,'Tejido silla','#eee9da');
function roundedBox(n,w,h,d,r){
 const positions=[],normals=[],indices=[],uvs=[],half=[w/2,h/2,d/2],N=10;
 for(let axis=0;axis<3;axis++)for(const sign of [-1,1]){const offset=positions.length/3,u=(axis+1)%3,v=(axis+2)%3;
  for(let j=0;j<=N;j++)for(let i=0;i<=N;i++){const p=[0,0,0];p[axis]=sign*half[axis];p[u]=(i/N*2-1)*half[u];p[v]=(j/N*2-1)*half[v];const q=p.map((a,k)=>Math.max(-half[k]+r,Math.min(half[k]-r,a)));const delta=p.map((a,k)=>a-q[k]),len=Math.hypot(...delta);positions.push(...q.map((a,k)=>a+delta[k]/len*r));normals.push(...delta.map(a=>a/len));uvs.push(i/N,j/N)}
  for(let j=0;j<N;j++)for(let i=0;i<N;i++){const a=offset+j*(N+1)+i,b=a+1,c=a+N+1,d=c+1;if(sign<0)indices.push(a,b,c,b,d,c);else indices.push(a,c,b,b,c,d)}
 }const mesh=new B.Mesh(n,scene),data=new B.VertexData();data.positions=positions;data.normals=normals;data.indices=indices;data.uvs=uvs;data.applyToMesh(mesh);return mesh;
}
function box(n,w,h,d,x,y,z,m,collision=true){const soft=/Sofá|Brazo|Silla|Reposacabezas|Reposapiés|Escritorio|Techo/.test(n);const o=soft?roundedBox(n,w,h,d,Math.min(w,h,d)*.24):B.MeshBuilder.CreateBox(n,{width:w,height:h,depth:d},scene);o.position.set(x,y,z);o.material=m;o.checkCollisions=collision;return o}
box('Suelo',3.4,.14,2.8,0,.07,0,pine);box('Alfombra',3.12,.04,2.51,0,.16,0,gray);box('Pared posterior',3.4,2.36,.12,0,1.32,1.34,wall);box('Lateral izquierdo',.13,2.3,2.8,-1.635,1.3,0,pine);box('Lateral derecho',.13,2.3,2.8,1.635,1.3,0,pine);box('Techo',3.2,.12,2.8,0,2.44,0,pine);
// Rounded continuous front frame, with a clear opening.
const framePoints=[];for(const [cx,cy,start] of [[1.35,2.15,0],[-1.35,2.15,90],[-1.35,.35,180],[1.35,.35,270]])for(let i=0;i<=12;i++){const a=(start+i*90/12)*Math.PI/180;framePoints.push(new B.Vector3(cx+.28*Math.cos(a),cy+.28*Math.sin(a),-1.4))}framePoints.push(framePoints[0]);const frame=B.MeshBuilder.CreateTube('Marco redondeado',{path:framePoints,radius:.085,tessellation:16},scene);frame.material=pine;
box('Cristal fijo',1.62,2.12,.025,-.78,1.28,-1.39,glass);const door=box('Puerta corredera',1.47,2.12,.025,.78,1.28,-1.43,glass);const handle=box('Tirador',.035,.48,.06,.19,1.25,-1.49,black);const handleOffset=handle.position.subtract(door.position);box('Guía superior',3.03,.045,.06,0,2.36,-1.42,black);box('Guía inferior',3.03,.035,.06,0,.2,-1.42,black);
box('Divisor opaco',.08,1.85,1.5,.12,1.105,.51,wall);
box('Escritorio',1.35,.065,.7,-.78,.93,.47,wood);for(const x of [-1.36,-.2])box('Pata escritorio',.035,.72,.035,x,.54,.35,black);
box('Silla asiento',.57,.14,.55,-.78,.62,.94,cream);box('Silla respaldo',.57,.7,.13,-.78,1.05,1.2,cream);box('Reposacabezas',.52,.23,.13,-.78,1.52,1.2,cream);box('Base silla',.55,.04,.5,-.78,.23,.94,black);box('Soporte silla',.07,.3,.07,-.78,.4,.94,black);box('Reposapiés',.48,.15,.35,-.78,.29,-.12,cream);
box('Portátil',.38,.025,.26,-.7,.978,.35,black);box('Sofá asiento',.95,.34,.9,.94,.41,.65,green);box('Sofá respaldo',.95,.57,.18,.94,.82,1.01,green);for(const x of [.5,1.38])box('Brazo sofá',.14,.49,.9,x,.6,.65,green);
for(let i=0;i<16;i++)box('Listón acústico',.052,2.1,.04,-1.51+i*.092,1.28,1.25,black);
box('Repisa',1.2,.05,.25,.91,1.92,1.12,wood);box('Luz superior',1.3,.025,.38,0,2.36,0,lamp,false);
function cylinder(n,diam,h,x,y,z,m){const o=B.MeshBuilder.CreateCylinder(n,{diameter:diam,height:h,tessellation:32},scene);o.position.set(x,y,z);o.material=m;o.checkCollisions=true;return o}
for(const [x,z,r,h] of [[.73,-.45,.48,.46],[1.15,-.25,.36,.59]]){cylinder('Mesa negra',r,.04,x,h,z,black);cylinder('Pata mesa',.05,h-.2,x,(h+.2)/2,z,black);const rim=B.MeshBuilder.CreateTorus('Borde elevado',{diameter:r-.02,thickness:.025,tessellation:40},scene);rim.position.set(x,h+.025,z);rim.material=black;}
const leaf=mat('Hojas','#648343');function plant(x,y,z,scale=1){cylinder('Maceta',.14*scale,.15*scale,x,y,z,cream);for(let i=0;i<7;i++){const o=B.MeshBuilder.CreateSphere('Hoja',{diameter:.16*scale,segments:8},scene);o.scaling.set(.5,1.4,.5);o.position.set(x+Math.sin(i)*.09*scale,y+.14*scale,z+Math.cos(i)*.07*scale);o.rotation.z=Math.sin(i)*.7;o.material=leaf}}
for(let i=0;i<5;i++)plant(.45+i*.22,2.01,1.1,.85);plant(1.15,.69,-.25);
const leds=[];for(const [x,z,w,d] of [[0,1.23,3.05,.018],[-1.55,0,.018,2.5],[1.55,0,.018,2.5],[.9,1.03,1.2,.018]]){const segments=12;for(let i=0;i<segments;i++){const m=leds[i] || mat('LED '+i,'#000000');m.disableLighting=true;const horizontal=w>d;box('Tira LED',horizontal?w/segments:w,.018,horizontal?d:d/segments,x+(horizontal?(i+.5)*w/segments-w/2:0),w===1.2?1.88:.24,z+(horizontal?0:(i+.5)*d/segments-d/2),m,false);if(!leds[i])leds.push(m)}}
function screen(n,w,h,x,y,z,rotation,text){const m=mat(n,'#132b24'),t=new B.DynamicTexture(n,{width:768,height:512},scene,true);const c=t.getContext();c.fillStyle='#122c24';c.fillRect(0,0,768,512);c.fillStyle='#e5efda';c.font='42px sans-serif';c.fillText('∩  Guarida',45,90);c.font='26px sans-serif';text.forEach((v,i)=>c.fillText(v,45,180+i*64));t.update();m.diffuseTexture=t;m.emissiveTexture=t;const s=B.MeshBuilder.CreatePlane(n,{width:w,height:h,sideOrientation:B.Mesh.DOUBLESIDE},scene);s.position.set(x,y,z);s.rotation.y=rotation;s.material=m;s.actionManager=new B.ActionManager(scene);s.actionManager.registerAction(new B.ExecuteCodeAction(B.ActionManager.OnPickTrigger,()=>onPanel(n==='Pantalla exterior'?'access':'assistant')));return s}
screen('Panel IA',.82,.57,-1.55,1.53,.25,-Math.PI/2,['Jade · Asistente de estudio','Mood · Música · Privacidad','Toca para comenzar']);screen('Pantalla exterior',.3,.34,1.52,1.35,-1.505,0,['Bienvenido','Abrir acceso']);
// No exterior ground: the cubicle floats against the hero background.

return {door,handle,handleOffset,glass,leds,lamp};
}


const THREE_URL = 'https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.min.js';

const PARTS = [
  {id:'sump',title:'Stainless sump',description:'The cylindrical shell accepts a 10- or 20-inch Jumbo/Big Blue cartridge. Relative form only; confirm dimensions for quotation.',source:'Published product page and main/inspection photos',inference:'observed'},
  {id:'head',title:'Cast filter head',description:'The head carries two opposed connection ports. Port size, thread standard and flow direction must be confirmed.',source:'Main and port-detail photos',inference:'observed-with-unconfirmed-specification'},
  {id:'connection-ports',title:'Connection ports',description:'Two threaded connections are shown without assigning inlet or outlet direction.',source:'Main and port-detail photos',inference:'observed-with-unconfirmed-specification'},
  {id:'clamp-ring',title:'Clamp ring',description:'The removable clamp joins the head and sump flanges. Maintenance order and pressure-isolation procedure require project confirmation.',source:'Main photo',inference:'observed'},
  {id:'wall-bracket',title:'Wall bracket',description:'The bracket represents the visible mounting plate and keyhole slots. Mounting loads and clearances are not engineering data.',source:'Main and port-detail photos',inference:'observed-with-unconfirmed-dimensions'},
  {id:'pressure-gauge',title:'Optional pressure gauge',description:'A gauge is an optional configuration shown for orientation only; range and connection are not specified.',source:'Published product facts and gauge-options photo',inference:'optional'},
  {id:'seal',title:'Illustrative seal',description:'The dark ring explains the sealing location in exploded view. Material, section and replacement specification remain to be confirmed.',source:'Inferred from clamped flange assembly',inference:'illustrative'},
  {id:'cartridge',title:'Illustrative cartridge',description:'The cartridge shows service access and is not a claim about the supplied media or internal socket geometry.',source:'Published 10/20-inch compatibility; internal geometry not photographed',inference:'illustrative'}
];

function labelled(mesh, id, label) {
  mesh.name = id;
  mesh.userData.partId = id;
  mesh.userData.partLabel = label;
  return mesh;
}

function addPart(root, group, id, label, explodeVector) {
  group.name = id;
  group.userData.partId = id;
  group.userData.partLabel = label;
  group.userData.home = group.position.clone();
  group.userData.explodeVector = explodeVector;
  group.traverse((node) => { if (node.isMesh) labelled(node, id, label); });
  root.add(group);
}

function createHousing(THREE) {
  const root = new THREE.Group();
  root.name = 'sus-304-jumbo-housing';
  const brushed = new THREE.MeshPhysicalMaterial({color:0xbcc2c3,metalness:1,roughness:.27,clearcoat:.12,clearcoatRoughness:.32});
  const cast = new THREE.MeshStandardMaterial({color:0xaeb5b6,metalness:.9,roughness:.42});
  const polished = new THREE.MeshPhysicalMaterial({color:0xd6dcdd,metalness:1,roughness:.18,clearcoat:.18});
  const rubber = new THREE.MeshStandardMaterial({color:0x263238,roughness:.82,metalness:0});
  const media = new THREE.MeshStandardMaterial({color:0xe8e4d7,roughness:.88,metalness:0});
  const steelBox = (w,h,d,m=polished) => new THREE.Mesh(new THREE.BoxGeometry(w,h,d,2,2,2),m);
  const sump = new THREE.Group();
  const shell = new THREE.Mesh(new THREE.CylinderGeometry(.72,.69,2.85,64,1,false),brushed); shell.position.y=-.82; sump.add(shell);
  const bottom = new THREE.Mesh(new THREE.SphereGeometry(.695,48,16,0,Math.PI*2,Math.PI/2,Math.PI/2),brushed); bottom.scale.y=.18; bottom.position.y=-2.25; sump.add(bottom);
  const lowerFlange = new THREE.Mesh(new THREE.CylinderGeometry(.86,.78,.17,64),polished); lowerFlange.position.y=.63; sump.add(lowerFlange);
  addPart(root,sump,'sump','Stainless sump',new THREE.Vector3(0,-1.05,0));

  const head = new THREE.Group();
  const headBody = new THREE.Mesh(new THREE.CylinderGeometry(.84,.84,.68,64),cast); headBody.position.y=.99; head.add(headBody);
  const shoulder = new THREE.Mesh(new THREE.CylinderGeometry(.68,.82,.22,64),cast); shoulder.position.y=1.43; head.add(shoulder);
  const upperFlange = new THREE.Mesh(new THREE.CylinderGeometry(.87,.84,.14,64),polished); upperFlange.position.y=.61; head.add(upperFlange);
  addPart(root,head,'head','Cast filter head',new THREE.Vector3(0,.72,0));

  const ports = new THREE.Group();
  [-1,1].forEach((side)=>{const collar=new THREE.Mesh(new THREE.CylinderGeometry(.23,.23,.58,32),polished);collar.rotation.z=Math.PI/2;collar.position.set(side*1.02,1.08,0);ports.add(collar);for(let i=0;i<5;i++){const ridge=new THREE.Mesh(new THREE.TorusGeometry(.238,.018,8,32),polished);ridge.rotation.y=Math.PI/2;ridge.position.set(side*(1.16+i*.07),1.08,0);ports.add(ridge)}});
  addPart(root,ports,'connection-ports','Connection ports',new THREE.Vector3(0,.18,0));

  const clamp = new THREE.Group();
  const ring = new THREE.Mesh(new THREE.TorusGeometry(.84,.075,12,64),polished); ring.rotation.x=Math.PI/2; ring.position.y=.68; clamp.add(ring);
  const latch=steelBox(.24,.18,.18);latch.position.set(.82,.68,0);clamp.add(latch);const hinge=steelBox(.18,.18,.2);hinge.position.set(-.82,.68,0);clamp.add(hinge);
  addPart(root,clamp,'clamp-ring','Clamp ring',new THREE.Vector3(.75,.15,0));

  const bracket = new THREE.Group();
  const foot=steelBox(.86,.12,.52);foot.position.set(0,1.58,-.12);bracket.add(foot);
  const upright=steelBox(.9,.78,.1);upright.position.set(0,1.98,-.34);bracket.add(upright);
  const notch=new THREE.Mesh(new THREE.TorusGeometry(.18,.045,8,24,Math.PI),rubber);notch.rotation.x=Math.PI/2;notch.position.set(0,2.34,-.28);bracket.add(notch);
  [-.29,.29].forEach(x=>{const slot=new THREE.Mesh(new THREE.CapsuleGeometry(.065,.16,4,12),rubber);slot.position.set(x,2.08,-.40);slot.scale.z=.25;bracket.add(slot)});
  [-.28,.28].forEach(x=>[-.1,.1].forEach(z=>{const bolt=new THREE.Mesh(new THREE.CylinderGeometry(.075,.075,.09,6),polished);bolt.position.set(x,1.65,z);bracket.add(bolt)}));
  addPart(root,bracket,'wall-bracket','Wall bracket',new THREE.Vector3(0,.65,-.45));

  const gauge = new THREE.Group();
  const stem=new THREE.Mesh(new THREE.CylinderGeometry(.06,.06,.28,16),polished);stem.position.y=1.77;gauge.add(stem);
  const dial=new THREE.Mesh(new THREE.CylinderGeometry(.28,.28,.11,40),polished);dial.rotation.x=Math.PI/2;dial.position.set(0,2.03,0);gauge.add(dial);
  const face=new THREE.Mesh(new THREE.CircleGeometry(.235,40),new THREE.MeshStandardMaterial({color:0xf3f6f5,roughness:.55}));face.position.set(0,2.03,.061);gauge.add(face);
  addPart(root,gauge,'pressure-gauge','Optional pressure gauge',new THREE.Vector3(0,1.05,0));

  const seal = new THREE.Group(); const oRing=new THREE.Mesh(new THREE.TorusGeometry(.73,.035,10,64),rubber);oRing.rotation.x=Math.PI/2;oRing.position.y=.62;seal.add(oRing);addPart(root,seal,'seal','Illustrative seal',new THREE.Vector3(0,.38,0));
  const cartridge = new THREE.Group(); const filter=new THREE.Mesh(new THREE.CylinderGeometry(.43,.43,2.25,48),media);filter.position.y=-.62;cartridge.add(filter);addPart(root,cartridge,'cartridge','Illustrative cartridge',new THREE.Vector3(0,-.45,0));
  root.userData.sculptRuntime={parts:PARTS.map(({id,title})=>({id,title})),explodable:true,clickable:true,accuracy:'structural-illustration'};
  return root;
}

export async function mountProduct3D(container, emit) {
  const THREE = await import(THREE_URL);
  const canvasWrap = container.querySelector('[data-product-3d-canvas]');
  const status = container.querySelector('[data-product-3d-status]');
  const list = container.querySelector('[data-product-3d-parts]');
  const explodeButton = container.querySelector('[data-product-3d-explode]');
  const resetButton = container.querySelector('[data-product-3d-reset]');
  if (!canvasWrap || !window.WebGLRenderingContext) throw new Error('webgl_unavailable');
  const renderer = new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1,2)); renderer.outputColorSpace=THREE.SRGBColorSpace; renderer.toneMapping=THREE.ACESFilmicToneMapping; renderer.toneMappingExposure=1.05;
  canvasWrap.appendChild(renderer.domElement);
  const scene=new THREE.Scene(); const camera=new THREE.PerspectiveCamera(36,1,.1,100);camera.position.set(5,2.3,7.5);
  scene.add(new THREE.HemisphereLight(0xffffff,0x60727a,2.1)); const key=new THREE.DirectionalLight(0xffffff,4.1);key.position.set(4,7,6);scene.add(key);const rim=new THREE.DirectionalLight(0xbfe9f4,2.4);rim.position.set(-5,3,-4);scene.add(rim);
  const model=createHousing(THREE);scene.add(model);const floor=new THREE.Mesh(new THREE.CircleGeometry(3.2,64),new THREE.MeshStandardMaterial({color:0xdde6e8,roughness:1}));floor.rotation.x=-Math.PI/2;floor.position.y=-2.43;scene.add(floor);
  const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();let selected=null,exploded=false,dragging=false,lastX=0,lastY=0,theta=.62,phi=.12,zoom=1;
  PARTS.forEach((part)=>{const li=document.createElement('li');const button=document.createElement('button');button.type='button';button.textContent=part.title;button.dataset.partId=part.id;button.addEventListener('click',()=>selectPart(part.id,true));li.appendChild(button);list.appendChild(li)});
  function selectPart(id,track=false){selected=id;const part=PARTS.find(x=>x.id===id);container.querySelectorAll('[data-part-id]').forEach(b=>b.setAttribute('aria-current',String(b.dataset.partId===id)));model.traverse(n=>{if(n.isMesh&&n.material?.emissive)n.material.emissive.setHex(n.userData.partId===id?0x164958:0x000000)});if(part){container.querySelector('[data-product-3d-part-title]').textContent=part.title;container.querySelector('[data-product-3d-part-copy]').textContent=part.description;status.textContent=`Selected: ${part.title}`;if(track)emit('3d-part-select',{partId:id})}}
  function applyExplode(){model.children.forEach(g=>{if(!g.userData.home)return;g.position.copy(g.userData.home).addScaledVector(g.userData.explodeVector,exploded?1:0)});explodeButton.setAttribute('aria-pressed',String(exploded));explodeButton.textContent=exploded?'Assemble':'Explode';status.textContent=exploded?'Exploded structural illustration':'Assembled structural illustration'}
  explodeButton.addEventListener('click',()=>{exploded=!exploded;applyExplode();emit('3d-explode',{state:exploded?'open':'closed'})});
  resetButton.addEventListener('click',()=>{theta=.62;phi=.12;zoom=1;exploded=false;applyExplode();selectPart('sump')});
  const canvas=renderer.domElement;canvas.addEventListener('pointerdown',e=>{dragging=true;lastX=e.clientX;lastY=e.clientY;canvas.setPointerCapture(e.pointerId)});canvas.addEventListener('pointermove',e=>{if(!dragging)return;theta+=(e.clientX-lastX)*.008;phi=Math.max(-.55,Math.min(.55,phi+(e.clientY-lastY)*.006));lastX=e.clientX;lastY=e.clientY});canvas.addEventListener('pointerup',e=>{dragging=false;canvas.releasePointerCapture(e.pointerId)});canvas.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(.72,Math.min(1.45,zoom+Math.sign(e.deltaY)*.08))},{passive:false});
  canvas.addEventListener('click',e=>{if(Math.abs(e.clientX-lastX)>4||Math.abs(e.clientY-lastY)>4)return;const r=canvas.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-((e.clientY-r.top)/r.height)*2+1);raycaster.setFromCamera(pointer,camera);const hit=raycaster.intersectObject(model,true)[0];if(hit?.object.userData.partId)selectPart(hit.object.userData.partId,true)});
  const resize=()=>{const w=canvasWrap.clientWidth,h=canvasWrap.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix()};new ResizeObserver(resize).observe(canvasWrap);resize();
  const animate=()=>{if(!container.isConnected){renderer.dispose();return}model.rotation.y=theta;model.rotation.x=phi;camera.position.setLength(9*zoom);camera.lookAt(0,-.15,0);renderer.render(scene,camera);requestAnimationFrame(animate)};selectPart('sump');animate();
}

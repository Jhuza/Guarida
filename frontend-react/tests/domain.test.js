import test from 'node:test';
import assert from 'node:assert/strict';
import { secondsLeft,clockText,endingSoon,voiceMood } from '../src/domain.js';
test('contador usa fecha límite y nunca muestra valores negativos',()=>{
 assert.equal(secondsLeft({deadline:11000},1000),10);
 assert.equal(secondsLeft({deadline:11000},12000),0);
 assert.equal(clockText(125),'02:05');
});
test('la pausa conserva tiempo pero no dispara aviso de fin',()=>{
 assert.equal(secondsLeft({remaining:200},5000),200);
 assert.equal(endingSoon({remaining:200},5000),false);
 assert.equal(endingSoon({deadline:205000},5000),true);
 assert.equal(endingSoon({deadline:400000},5000),false);
 assert.equal(endingSoon({deadline:4000},5000),false);
});
test('voz solo reconoce los ambientes soportados',()=>{
 assert.equal(voiceMood('Quiero estudiar'),'concentracion');
 assert.equal(voiceMood('Descansar un rato'),'descanso');
 assert.equal(voiceMood('modo gamer'),'gamer');
 assert.equal(voiceMood('Abre mi correo'),null);
});

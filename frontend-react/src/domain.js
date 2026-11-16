export const moods = {
  disponible: { name: 'Bienvenida', description: 'Un inicio cálido', color: '#dcb967', palette: ['#ffd777'] },
  concentracion: { name: 'Estudio', description: 'Encuentra tu enfoque', color: '#699de1', palette: ['#659eff'] },
  gamer: { name: 'Ocio', description: 'Juega a tu ritmo', color: '#bc7bb1', palette: ['#ffdc65','#f65b58','#ed79be','#649cff'] },
  descanso: { name: 'Descanso', description: 'Date una pausa', color: '#78a583', palette: ['#79c78b'] },
};
export function secondsLeft(snapshot, now = Date.now()) {
  return Math.max(0, Math.ceil(snapshot.deadline ? (snapshot.deadline - now) / 1000 : Number(snapshot.remaining || 0)));
}
export function clockText(seconds) {
  const safe = Math.max(0, Math.ceil(Number(seconds) || 0));
  return `${Math.floor(safe/60).toString().padStart(2,'0')}:${(safe%60).toString().padStart(2,'0')}`;
}
export function endingSoon(snapshot, now = Date.now()) {
  const remaining = secondsLeft(snapshot, now);
  return !!snapshot.deadline && remaining > 0 && remaining <= 300;
}
export function voiceMood(text) {
  const value = text.toLowerCase();
  return /descans|relaja/.test(value) ? 'descanso' : /estudi|concentr/.test(value) ? 'concentracion' : /gamer|ocio/.test(value) ? 'gamer' : /bienvenida|disponible/.test(value) ? 'disponible' : null;
}

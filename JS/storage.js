// storage.js - Encapsula la persistencia en localStorage
const Storage = (function(){
const KEY = 'tickets_vortex';


function load(){
try{ return JSON.parse(localStorage.getItem(KEY) || '[]'); }
catch(e){ console.error('Error parseando tickets:', e); return []; }
}


function save(list){
localStorage.setItem(KEY, JSON.stringify(list));
}


function add(ticket){
const list = load();
list.push(ticket);
save(list);
return ticket;
}


function clear(){
localStorage.removeItem(KEY);
}


return { load, save, add, clear };
})();


// Hacer disponible en window para debugging
window.Storage = Storage;
export const BACKEND_URL = 'http://127.0.0.1:5000';

export const formatAmount = (amount) => {
  return '$'+amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

export const convertUTCDateToLocalDate = (date) => {
  var newDate = new Date(date.getTime()+date.getTimezoneOffset()*60*1000);

  var offset = date.getTimezoneOffset() / 60;
  var hours = date.getHours();

  newDate.setHours(hours - offset);

  return newDate;   
}

export const getData = async (url) => {
  const dataJson = fetch(url)
    .then((res) => {
      if (res.status === 200) {
        return res.json();
      }
      return null;
    })
    .catch(() => {
      return null;
    });
  return dataJson;
}

export function shortOpExpSubtype (subtype) {
  switch (subtype) {
    case 'Web y Almacenamiento':
      return 'Web y Almacenamiento';
    case 'Traspaso desde gastos operacionales a asignación personal de apoyo':
      return 'Traspaso a P.A.';
    case 'Traslación':
      return 'Traslación y Bencina';
    case 'Seguros de bienes':
      return 'Seguros';
    case 'Otros gastos de oficina parlamentaria':
      return 'Otros Oficina';
    case 'Actividades destinadas a la interacción con la comunidad':
      return 'Interacción Comunidad';
    default:
      return subtype;
  }
}
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
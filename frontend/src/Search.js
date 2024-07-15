import axios from "axios";

async function searchPlayer(input) {
  const corsAnywhereUrl = "https://cors-anywhere.herokuapp.com/";
  const searchUrl = "https://pixels-server.pixels.xyz/v1/player/search?input=";
  const url = corsAnywhereUrl + searchUrl + encodeURIComponent(input);

  let data;

  try {
    const response = await axios.get(url, {
      headers: {
        'Origin': 'https://54896a0b-b06b-4669-92f4-9b6e5dab3edd-00-1vpbsnrs1y5x9.spock.replit.dev:5000/' // Replace with your website's origin
      }
    });
    data = response.data;
  } catch (error) {
    console.error("Error looking up input:", error);
  }

  return data;
}

export default searchPlayer;
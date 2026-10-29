import {continueRender, delayRender} from 'remotion';
import '@fontsource/montserrat/600.css';
import '@fontsource/montserrat/700.css';
import '@fontsource/montserrat/800.css';
import '@fontsource/manrope/500.css';
import '@fontsource/manrope/600.css';
import '@fontsource/manrope/700.css';

// Block rendering until every weight is really loaded (otherwise frame 0 can render with a fallback font).
const handle = delayRender('Loading fonts');
const sample = 'WAGGA abc ABC & — ’!.,0123456789';
Promise.all([
  document.fonts.load('600 40px Montserrat', sample),
  document.fonts.load('700 40px Montserrat', sample),
  document.fonts.load('800 40px Montserrat', sample),
  document.fonts.load('500 30px Manrope', sample),
  document.fonts.load('600 30px Manrope', sample),
  document.fonts.load('700 30px Manrope', sample),
])
  .then(() => continueRender(handle))
  .catch(() => continueRender(handle));

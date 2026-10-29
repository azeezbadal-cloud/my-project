import React from 'react';
import {AbsoluteFill} from 'remotion';
import './fonts';
import {colors} from './theme';
import {useT} from './lib/useT';
import {VideoStage} from './components/VideoStage';
import {Overlay} from './components/Overlay';
import {Welcome} from './scenes/Welcome';
import {NowOpen} from './scenes/NowOpen';
import {Services} from './scenes/Services';
import {Expansion} from './scenes/Expansion';
import {Outro} from './scenes/Outro';

/**
 * Layer order (bottom → top)
 *   blurred fill  →  graded background footage  →  atmosphere (streaks/particles)  →  glass banners
 *   →  speaker cut-out (sharp, with rim light)  →  stage graphics (map, logo)  →  finishing overlay
 */
export const Promo: React.FC = () => {
  const {t} = useT();
  return (
    <AbsoluteFill style={{backgroundColor: colors.navyDeep}}>
      <VideoStage
        t={t}
        behind={
          <>
            <Welcome />
            <NowOpen />
            <Services />
          </>
        }
      />
      <Expansion />
      <Outro />
      <Overlay t={t} />
    </AbsoluteFill>
  );
};

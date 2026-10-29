import React from 'react';
import {Composition} from 'remotion';
import {config} from './config';
import {Promo} from './Promo';

export const Root: React.FC = () => (
  <>
    <Composition
      id="WWCCPromo"
      component={Promo}
      durationInFrames={config.durationInFrames}
      fps={config.fps}
      width={config.width}
      height={config.height}
    />
  </>
);

import {useCurrentFrame, useVideoConfig} from 'remotion';

/** Current frame, fps and time in seconds. */
export const useT = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return {frame, fps, t: frame / fps};
};

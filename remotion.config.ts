import {Config} from '@remotion/cli/config';

// Frames are rendered as PNG so glass/blur gradients stay band-free before the final H.264 encode.
Config.setVideoImageFormat('png');
Config.setOverwriteOutput(true);

/**
 * WWCC promo – EVERYTHING you are likely to edit lives in this file:
 * on-screen text, timings (seconds), colours, services, expansion locations, contact details.
 *
 * After changing anything:  npm run studio   (live preview)   or   npm run render   (final MP4)
 */

export type IconName =
  | 'HandHeart'
  | 'UsersRound'
  | 'Car'
  | 'ShoppingBag'
  | 'SprayCan'
  | 'MessageCircleHeart'
  | 'MoonStar';

export type AccentName = 'blue' | 'green' | 'aqua' | 'gold';

export type ServiceItem = {
  /** One string per line – you control the line breaks. */
  lines: [string, string];
  /** Any icon name exported by the `lucide` package that is registered in src/components/Icon.tsx */
  icon: IconName;
  accent: AccentName;
};

export type City = {
  name: string;
  lat: number;
  lon: number;
  /** Which side of the pin its label sits on. */
  labelSide: 'left' | 'right';
  /** Nudge the label vertically (px) so neighbouring labels never collide. */
  labelDy?: number;
};

export type Contact = {
  /** Only shown when you fill them in. Nothing is invented – leave empty to hide. */
  website?: string;
  phone?: string;
  email?: string;
  /** Path of a QR code image inside /public, e.g. 'qr.png' */
  qrImage?: string;
};

export const config = {
  // ── Video format ────────────────────────────────────────────────────────────
  fps: 30,
  width: 1080,
  height: 1920,
  /** 22.933 s – matches the original footage (22.935 s). */
  durationInFrames: 688,

  // ── Files (inside /public) ──────────────────────────────────────────────────
  files: {
    footage: 'footage.mp4', // produced by: npm run prepare
    speaker: 'fg.webm', // speaker cut-out with transparency (optional depth effect)
    logo: 'logo.png',
  },
  /** Put light trails / glass *behind* the speaker using the cut-out. Set false to skip it. */
  useSpeakerCutout: true,

  // ── Brand colours ───────────────────────────────────────────────────────────
  colors: {
    navy: '#002078', // WWCC navy (sampled from the logo)
    navyDeep: '#040F33',
    navyMid: '#0A2A8F',
    blue: '#0070C0', // WWCC blue
    brightBlue: '#2D9CFF',
    sky: '#8AD4FF',
    emerald: '#10B981',
    green: '#008008', // WWCC green
    mint: '#5CF0B0',
    gold: '#F8B000',
    goldSoft: '#FFE2A0',
    white: '#FFFFFF',
  },
  fonts: {
    display: 'Montserrat', // headlines
    body: 'Manrope', // sub-lines
  },

  /** Keep text inside this box (Instagram/Facebook Reels + TikTok UI sits outside it). */
  safe: { top: 276, left: 64, right: 64, bottom: 440 },

  /** The footage shrinks into a floating window for the map + ending so there is room for graphics. */
  window: { scale: 0.6, bottom: 56, radius: 56, seconds: 0.95 },

  // ── 00:00 – 00:03  Welcome ──────────────────────────────────────────────────
  welcome: {
    start: 0,
    end: 3,
    eyebrow: 'WELCOME TO OUR COMMUNITY',
    title: ['WAGGA WAGGA', 'COMMUNITY CARE'] as [string, string],
  },

  // ── 00:03 – 00:06  Official announcement ────────────────────────────────────
  open: {
    start: 3,
    end: 6,
    headline: 'WE’RE NOW OPEN!',
    subline: 'Welcoming participants in Wagga Wagga, NSW',
  },

  // ── 00:06 – 00:14  Our services ─────────────────────────────────────────────
  services: {
    start: 6,
    end: 14,
    heading: ['SUPPORT THAT MAKES', 'A DIFFERENCE'] as [string, string],
    /** How long the heading holds before the cards start (seconds). */
    headingSeconds: 1.35,
    items: [
      {lines: ['Daily Living &', 'Personal Care'], icon: 'HandHeart', accent: 'blue'},
      {lines: ['Community Access &', 'Social Activities'], icon: 'UsersRound', accent: 'green'},
      {lines: ['Transport &', 'Appointments'], icon: 'Car', accent: 'aqua'},
      {lines: ['Shopping &', 'Domestic Assistance'], icon: 'ShoppingBag', accent: 'gold'},
      {lines: ['Cleaning &', 'Household Support'], icon: 'SprayCan', accent: 'blue'},
      {lines: ['Social Support &', 'Companionship'], icon: 'MessageCircleHeart', accent: 'green'},
      {lines: ['Overnight &', 'Sleepover Support'], icon: 'MoonStar', accent: 'aqua'},
    ] as ServiceItem[],
  },

  // ── 00:14 – 00:19  Our future expansion ─────────────────────────────────────
  expansion: {
    start: 14,
    end: 19,
    kicker: 'STARTING IN WAGGA WAGGA',
    next: 'OUR NEXT CHAPTER',
    badge: 'Planned Expansion',
    home: {name: 'WAGGA WAGGA', lat: -35.1082, lon: 147.3598},
    /** Cities are revealed one after another, in this order. */
    cities: [
      {name: 'TOOWOOMBA', lat: -27.5598, lon: 151.9507, labelSide: 'left'},
      {name: 'NEWCASTLE', lat: -32.9283, lon: 151.7817, labelSide: 'right', labelDy: -16},
      {name: 'SYDNEY', lat: -33.8688, lon: 151.2093, labelSide: 'right', labelDy: 22},
      {name: 'COFFS HARBOUR', lat: -30.2963, lon: 153.1135, labelSide: 'right'},
    ] as City[],
    cityStart: 15.75,
    cityStep: 0.72,
  },

  // ── 00:19 – end  Branded ending ─────────────────────────────────────────────
  outro: {
    start: 19,
    end: 22.9333,
    tagline: 'YOUR GOALS. OUR SUPPORT.',
    cta: 'ENQUIRE TODAY',
    /** The logo artwork already contains the name and "Supporting Independence. Building Community." */
    contact: {} as Contact,
  },
};

export type Config = typeof config;

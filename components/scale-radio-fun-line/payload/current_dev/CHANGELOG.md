0.4.0
- fixed settings-page backend crash (`.catch` instead of `.fail`)
- added `SDL_AUDIODRIVER=dummy` in service, launcher and renderer
- service preload now waits for `runtime/service_enabled.flag` written by `onStart`
- service no longer keeps running when plugin is inactive at boot
- default framing tuned: lower baseline, larger actors

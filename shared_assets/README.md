# lite-shared-assets

## SVG Icons

The LITE projects use SVGs for icons. This has several benefits:

* Infinite scalability
* Smaller size
* Ability to recolour

#### To use LITE SVGs in your project:

Add ```os.path.join(BASE_DIR, 'lite-shared-assets/lite-frontend/assets/images'),``` to ```SVG_DIRS``` in your settings file.

This requires [django-inline-svg](https://github.com/mixxorz/django-inline-svg).
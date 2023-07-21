## Spectrometer codes

# Requirements

'''pip install seabreeze numpy scipy matplotlib gpiozero '''

# Definition of main functions used

'''
def wavelengths(self):
    - wavelength array of the spectrometer

    wavelengths in (nm) corresponding to each pixel of the spectrometer

    Returns
    -------
    wavelengths : `numpy.ndarray`
        wavelengths in (nm)
    return self._wavelengths

def intensities(self, correct_dark_counts=False, correct_nonlinearity=False):
    - measured intensity array in (a.u.)

    Measured intensities as numpy array returned by the spectrometer.
    The measuring behavior can be adjusted by setting the trigger mode.
    Pixels at the start and end of the array might not be optically
    active so interpret their returned measurements with care. Refer
    to the spectrometer's datasheet for further information.

    Notes
    -----
    Intensities are in arbitrary units and the range depends on the
    ADC bit resolution of the hardware used in the specific spectrometer.
    Some spectrometers store a `saturation` value in their eeprom,
    which is used to rescale the raw ADC output to the full bit range.
    (This is done in `libseabreeze` and therefore also in `cseabreeze`
    --- for compatibility reasons the same is done in `pyseabreeze`)
    I.e. this means that a 16bit (max value 65535) spectrometer with a
    saturation value of ~30000 is effectively only returning ~15bit
    resolution raw readings. While most of the lower bits are dominated
    by noise anyways, it's just something to keep in mind. Refer to
    `pyseabreeze.features.spectrometer._SeaBreezeSpectrometerSaturationMixin`
    for the implementation.

    Parameters
    ----------
    correct_dark_counts : `bool`
        If requested and supported the average value of electric dark
        pixels on the ccd of the spectrometer is subtracted from the
        measurements to remove the noise floor in the measurements
        caused by non optical noise sources.
    correct_nonlinearity : `bool`
        Some spectrometers store non linearity correction coefficients
        in their eeprom. If requested and supported by the spectrometer
        the readings returned by the spectrometer will be linearized
        using the stored coefficients.

    Returns
    -------
    intensities : `numpy.ndarray`
        measured intensities in (a.u.)
    """
    if correct_dark_counts and not self._dp:
        raise self._backend.SeaBreezeError(
            "This device does not support dark count correction."
        )
    if correct_nonlinearity and not self._nc:
        raise self._backend.SeaBreezeError(
            "This device does not support nonlinearity correction."
        )
    # Get the intensities
    out = self._dev.f.spectrometer.get_intensities()
    # Do corrections if requested
    if correct_nonlinearity or correct_dark_counts:
        dark_offset = numpy.mean(out[self._dp]) if self._dp else 0.0
        out -= dark_offset
    if correct_nonlinearity:
        out = out / numpy.polyval(self._nc, out)
    if correct_nonlinearity and (not correct_dark_counts):
        # noinspection PyUnboundLocalVariable
        out += dark_offset
    return out
'''

# MIT License

Copyright (c) <2022> <Clodoaldo de Souza Faria Júnior>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
 

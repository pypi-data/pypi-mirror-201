from contextlib import contextmanager

import numpy as np

from wellgui.exceptions import InvalidCurveException


class IrregularlySpacedCurve:
    def __init__(self):
        self._check_length_consistency = True
        self._data = np.asarray([], dtype=float)
        self._index = np.asarray([], dtype=float)
    
    @contextmanager
    def ignore_inconsistent_lengths(self):
        try:
            self._check_length_consistency = False
            yield self
        finally:
            self._check_length_consistency = True

    def _check_validity(self):
        failures = []
        if len(self.data) != len(self.index):
            failures.append(f"index length ({len(self.index)}) must equal data length ({len(self.data)})")
        if self.index.ndim != 1:
            failures.append(f"index dimensionality ({self.index.ndim}) must be 1")
        return failures
    
    def _assert_validity(self):
        failures = self._check_validity()
        if failures:
            raise InvalidCurveException("; ".join(failures))

    def set_data_with_index(self, index, data):
        with self.ignore_inconsistent_lengths() as self:
            self.index = index
            self.data = data
        self._assert_validity()

    def set_data_from_series(self, series):
        with self.ignore_inconsistent_lengths() as self:
            self.index = series.index.values
            self.data = series.values
        self._assert_validity()

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, values):
        values = np.asarray(values)
        if self._check_length_consistency:
            if len(values) != len(self.data):
                raise InvalidCurveException(f"data length ({len(values)}) must equal index length ({len(self.index)})")
        self._index = values

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, values):
        if self._check_length_consistency:
            if len(values) != len(self.index):
                raise InvalidCurveException(f"index length ({len(self.index)}) must equal data length ({len(values)})")
        self._data = values



class RegularlySpacedCurve(IrregularlySpacedCurve):
    def __init__(self):
        super(RegularlySpacedCurve, self).__init__()

    def _check_validity(self):
        failures = super(RegularlySpacedCurve, self)._check_validity()
        index_spacings = np.diff(self.index)
        
        # Deal with floating point arithmetic e.g. 0.049999999999991 != 0.05
        index_spacings = [np.round(x, 6) for x in index_spacings]

        if len(set(index_spacings)) > 1:
            failures.append(f"index spacing must be constant ({set(index_spacings)})")
        return failures

    @property
    def spacing(self):
        return np.diff(self.index)[0]

    @spacing.setter
    def spacing(self, new_spacing):
        # This means interpolating or up-scaling the curve.
        if new_spacing > self.spacing:
            message = "Downsampling not yet implemented"
        elif new_spacing < self.spacing:
            message = "Interpolation not yet implemented"
        raise NotImplementedError(message)

    
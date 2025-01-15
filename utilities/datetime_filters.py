from rangefilter.filters import DateRangeFilter

date_filters = (('created_at', DateRangeFilter),
                ('modified_at', DateRangeFilter),
                ('deleted', DateRangeFilter),)

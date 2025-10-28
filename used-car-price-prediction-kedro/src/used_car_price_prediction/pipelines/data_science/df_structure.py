category_columns = [
    'car_name',
    'yr_mfr',
    'fuel_type',
    'city',
    'body_type',
    'transmission',
    'variant',
    'registered_state',
    'registered_city',
    'rto',
    'source',
    'make',
    'model',
    'car_availability',
    'car_rating'
]

numeric_columns = [
    'kms_run',
    'sale_price',
    'times_viewed',
    'total_owners',
    'broker_quote',
    'original_price',
    'emi_starts_from',
    'booking_down_pymnt'
]

boolean_columns = [
    'assured_buy',
    'is_hot',
    'fitness_certificate',
    'reserved',
    'warranty_avail'
]

other_columns = [
    'ad_created_on'
]

columns = {
    'CATEGORICAL':category_columns,
    'NUMERIC':numeric_columns,
    'BOOLEAN':boolean_columns,
    'OTHER':other_columns
}

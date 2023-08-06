function construct_query_string(loc, query_params=[], only_query_string=false) {
    // empty values will be removed
    let query_string = only_query_string? '': loc.pathname;
    let encoded_params = [];
    query_params.sort(function(elem1, elem2) {
        if (elem1[0] < elem2[0]) {
            return -1;
        } else if (elem1[0] > elem2[0]) {
            return 1;
        } else {
            if (elem1[1] < elem2[1]) {
                return -1;
            } else if (elem1[1] > elem2[1]) {
                return 1;
            }
        }
        return 0;
    });
    query_params.forEach(function(key_value) {
        if (typeof key_value[1] !== 'undefined') {
            encoded_params.push(encodeURI(key_value[0]) + '=' + encodeURI(key_value[1]));
        }
    });
    query_string += '?' + encoded_params.join('&');
    return query_string;
}


function parse_query_parameters(loc) {
    let params = [];
    let key_value;
    let pairs = loc.search.replace('?', '').split('&');
    pairs.forEach(function(element) {
        key_value = element.split('=');
        params.push([decodeURI(key_value[0]), decodeURI(key_value[1])]);
    });
    return params;
}


function modify_query(loc, params_to_remove=[], params_to_change={}, only_query_string=false) {
    /* Returns a link with modified current query parameters */
    let query_params = [];
    let get_data = parse_query_parameters(loc);

    get_data.forEach(function(key_value) {
        let key = key_value[0];
        let value = key_value[1];
        if (params_to_remove.indexOf(key) === -1) {
            if (typeof params_to_change[key] !== 'undefined') {
                // skip query_params
            } else {
                // leave existing parameters as they were
                // if not mentioned in the params_to_change
                get_data.forEach(function(element) {
                    if (element[0] === key) {
                        query_params.push([key, element[1]])
                    }
                });
            }
        }
    });
    for (let key in params_to_change) {
        if (params_to_change.hasOwnProperty(key)) {
            query_params.push([key, params_to_change[key]]);
        }
    }
    return construct_query_string(loc, query_params, only_query_string);
}


function add_to_query(loc, params_to_remove=[], params_to_add={}, only_query_string=false) {
    /* Returns a link with modified current query parameters */
    let query_params = [];
    // go through current query params..
    let get_data = parse_query_parameters(loc);

    get_data.forEach(function(key_value) {
        let key = key_value[0];
        let value = key_value[1];
        if (params_to_remove.indexOf(key) === -1) {
            query_params.push([key, value]);
        }
    });
    // add the rest key-value pairs
    for (let key in params_to_add) {
        if (params_to_add.hasOwnProperty(key)) {
            query_params.push([key, params_to_add[key]]);
        }
    }
    return construct_query_string(loc, query_params, only_query_string);
}


function remove_from_query(loc, args=[], kwargs={}, only_query_string=false) {
    /* Returns a link with modified current query parameters */
    let query_params = [];
    // go through current query params..
    let get_data = parse_query_parameters(loc);

    get_data.forEach(function(key_value) {
        let key = key_value[0];
        let value = key_value[1];
        if (args.indexOf(key) === -1) {
            if (typeof kwargs[key] === 'undefined' || value !== kwargs[key].toString()) {
                // skip key-value pairs mentioned in kwargs
                query_params.push([key, value]);
            }
        }
    });
    return construct_query_string(loc, query_params, only_query_string);
}
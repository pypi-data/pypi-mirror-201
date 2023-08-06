QUnit.test('construct_query_string() test', function(assert) {
    let loc = {
        pathname: '/en/test/'
    };
    let query_params = [['a', '1'], ['a', 2], ['b', 3], ['c', 'OK'], ['d', 'Hello, World!']];
    let query = construct_query_string(loc, query_params);
    assert.ok(query === '/en/test/?a=1&a=2&b=3&c=OK&d=Hello,%20World!', 'Passed!');
});


QUnit.test('construct_query_string() only query string test', function(assert) {
    let loc = {
        pathname: '/en/test/'
    };
    let query_params = [['a', '1'], ['a', 2], ['b', 3], ['c', 'OK'], ['d', 'Hello, World!']];
    let query = construct_query_string(loc, query_params, true);
    assert.ok(query === '?a=1&a=2&b=3&c=OK&d=Hello,%20World!', 'Passed!');
});


QUnit.test('parse_query_parameters() test', function(assert) {
    let loc = {
        search: '?a=1&a=2&b=3&c=OK&d=Hello,%20World!'
    };
    let query_params = parse_query_parameters(loc);
    let expected_result = [['a', '1'], ['a', '2'], ['b', '3'], ['c', 'OK'], ['d', 'Hello, World!']];
    assert.ok(JSON.stringify(query_params) === JSON.stringify(expected_result), 'Passed!');
});


QUnit.test('modify_query(loc, params_to_remove=[], params_to_change={}) test', function(assert) {
    let loc = {
        pathname: '/en/test/',
        search: '?a=1&a=2&b=3&c=OK&d=Hello,%20World!'
    };
    let path = modify_query(loc, params_to_remove=['c'], params_to_change={'a': 3, 'b': 4});
    let expected_result = '/en/test/?a=3&b=4&d=Hello,%20World!';
    assert.ok(path === expected_result, 'Passed!');
});


QUnit.test('modify_query(loc, params_to_remove=[], params_to_change={}) only query string test', function(assert) {
    let loc = {
        pathname: '/en/test/',
        search: '?a=1&a=2&b=3&c=OK&d=Hello,%20World!'
    };
    let path = modify_query(loc, params_to_remove=['c'], params_to_change={'a': 3, 'b': 4}, only_query_string=true);
    let expected_result = '?a=3&b=4&d=Hello,%20World!';
    assert.ok(path === expected_result, 'Passed!');
});


QUnit.test('add_to_query(loc, params_to_remove=[], params_to_add={}) test', function(assert) {
    let loc = {
        pathname: '/en/test/',
        search: '?a=1&a=2&b=3&c=OK&d=Hello,%20World!'
    };
    let path = add_to_query(loc, params_to_remove=['c'], params_to_add={'a': 3, 'b': 4});
    let expected_result = '/en/test/?a=1&a=2&a=3&b=3&b=4&d=Hello,%20World!';
    assert.ok(path === expected_result, 'Passed!');
});


QUnit.test('add_to_query(loc, params_to_remove=[], params_to_add={}) only query string test', function(assert) {
    let loc = {
        pathname: '/en/test/',
        search: '?a=1&a=2&b=3&c=OK&d=Hello,%20World!'
    };
    let path = add_to_query(loc, params_to_remove=['c'], params_to_add={'a': 3, 'b': 4}, only_query_string=true);
    let expected_result = '?a=1&a=2&a=3&b=3&b=4&d=Hello,%20World!';
    assert.ok(path === expected_result, 'Passed!');
});


QUnit.test('remove_from_query(loc, args=[], kwargs={}) test', function(assert) {
    let loc = {
        pathname: '/en/test/',
        search: '?a=1&a=2&b=3&c=OK&d=Hello,%20World!'
    };
    let path = remove_from_query(loc, args=['c'], kwargs={'a': 2});
    let expected_result = '/en/test/?a=1&b=3&d=Hello,%20World!';
    assert.ok(path === expected_result, 'Passed!');
});


QUnit.test('remove_from_query(loc, args=[], kwargs={}) only query string test', function(assert) {
    let loc = {
        pathname: '/en/test/',
        search: '?a=1&a=2&b=3&c=OK&d=Hello,%20World!'
    };
    let path = remove_from_query(loc, args=['c'], kwargs={'a': 2}, only_query_string=true);
    let expected_result = '?a=1&b=3&d=Hello,%20World!';
    assert.ok(path === expected_result, 'Passed!');
});

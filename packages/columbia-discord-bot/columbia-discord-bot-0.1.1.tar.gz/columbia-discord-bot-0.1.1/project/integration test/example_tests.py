'''
    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN
'''

import sys
import dismock

# The tests themselves

testcollector = dismock.TestCollector()


@testcollector()
async def test_ping(interface):
    await interface.assert_reply_equals('!ping', 'pong!')


@testcollector()
async def test_add_class(interface):
    await interface.assert_reply_equals('!addclass COMS0000', 'Added class!')


# Make it easy to run the tests

if __name__ == '__main__':
    _, target_name, token = sys.argv
    dismock.run_interactive_bot(target_name, token, testcollector)

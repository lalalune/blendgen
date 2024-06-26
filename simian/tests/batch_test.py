from ..batch import render_objects


def test_render_objects():
    """
    Test the render_objects function.
    """
    processes = 4
    render_timeout = 3000
    width = 1920
    height = 1080
    start_index = 0
    end_index = 1
    start_frame = 1
    end_frame = 2

    # Call the function
    try:
        render_objects(
            processes=processes,
            render_timeout=render_timeout,
            width=width,
            height=height,
            start_index=start_index,
            end_index=end_index,
            start_frame=start_frame,
            end_frame=end_frame,
        )
        print("============ Test Passed: render_objects ============")
    except Exception as e:
        print("============ Test Failed: render_objects ============")
        print(f"Error: {e}")
        raise e


if __name__ == "__main__":
    test_render_objects()
    print("============ ALL TESTS PASSED ============")

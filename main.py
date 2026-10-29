
from service import check_service_status


def main():
    print("PT436 - Mutation Testing Framework")
    print("----------------------------------")

    status = 200
    result = check_service_status(status)

    print(f"Service status code: {status}")
    print(f"Service is healthy: {result}")


if __name__ == "__main__":
    main()

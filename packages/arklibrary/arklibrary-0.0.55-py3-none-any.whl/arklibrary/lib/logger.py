class Logger:
    LABEL_WIDTH = 11
    SPACING = 3

    def __init__(self):
        self.__messages = []
        self.__has_errors = False
        self.__is_testing = False

    @property
    def is_testing(self):
        return self.__is_testing

    @property
    def has_errors(self):
        return self.__has_errors

    def messages(self):
        return '\n'.join(self.__messages)

    def __enter__(self):
        self.__is_testing = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.has_errors:
            for message in self.__messages:
                print(message)

    def error(self, message: str, **kwargs):
        label = "ERROR".center(Logger.LABEL_WIDTH)
        spacing = " " * Logger.SPACING
        colored_label = f"\033[0;1;41m{label}\033[0m"
        output = f"{colored_label}{spacing}\033[31m{message}\033[0m"
        self.__messages.append(output)
        self.__has_errors = True
        if not self.is_testing:
            print(output)
            return output

    def success(self, message, **kwargs):
        label = "SUCCESS".center(Logger.LABEL_WIDTH)
        spacing = " " * Logger.SPACING
        colored_label = f"\033[0;1;42m{label}\033[0m"
        output = f"{colored_label}{spacing}\033[32m{message}\033[0m"
        self.__messages.append(output)
        if not self.is_testing:
            print(output)
            return output

    def warning(self, message, **kwargs):
        label = "WARNING".center(Logger.LABEL_WIDTH)
        spacing = " " * Logger.SPACING
        colored_label = f"\033[0;1;43m{label}\033[0m"
        output = f"{colored_label}{spacing}\033[33m{message}\033[0m"
        self.__messages.append(output)
        if not self.is_testing:
            print(output)
            return output

    def log(self, message, **kwargs):
        label = "LOG".center(Logger.LABEL_WIDTH)
        spacing = " " * Logger.SPACING
        colored_label = f"\033[0;1;47m{label}\033[0m"
        output = f"{colored_label}{spacing}\033[37m{message}\033[0m"
        self.__messages.append(output)
        if not self.is_testing:
            print(output)
            return output

    def variables(self, **values):
        label = "VARIABLE".center(Logger.LABEL_WIDTH)
        spacing = " " * Logger.SPACING
        colored_label = f"\033[0;1;44m{label}\033[0m"
        for var_name, var_value in values.items():
            output = f"{colored_label}{spacing}\033[34m{var_name} = {repr(var_value)}\033[0m"
            self.__messages.append(output)
        if not self.is_testing:
            result = '\n'.join(self.__messages[-len(values):])
            print(result)
            return result

    def condition(self, statement, result, **kwargs):
        label = "CONDITION".center(Logger.LABEL_WIDTH)
        spacing = " " * Logger.SPACING
        colored_label = f"\033[0;1;45m{label}\033[0m"
        output = f"{colored_label}{spacing}\033[35m{statement} : {result}\033[0m"
        self.__messages.append(output)
        if not self.is_testing:
            print(output)
            return output


if __name__ == "__main__":
    log = Logger()
    log.error("an error occurred")
    log.warning("a warning occurred")
    log.success("something has passed")
    log.variables(value='string value')
    log.log('a simple log')
    log.condition('if a > 0', True)
    print("\n\n\n")

    print("-----------Should not have anything after here ----------")
    with Logger() as log:
        log.warning("a warning occurred")
        log.success("something has passed")
        log.variables(value='string value')
        log.log('a simple log')
        log.condition('if a > 0', True)
    print("-----------Should not have anything before here ----------\n\n\n\n")

    with Logger() as log:
        log.error("an error occurred")
        log.warning("a warning occurred")
        log.success("something has passed")
        log.variables(value='string value')
        log.log('a simple log')
        log.condition('if a > 0', True)


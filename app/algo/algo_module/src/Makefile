
.PHONY: all clean fclean re

NAME = debug

SRCS_LIST = minmax_init.c estimate.c helpers.c minmax.c steps.c debug_main.c
# HEADERS_LIST = scop.h

# SRCS = $(addprefix $(SRC_DIR),$(SRCS_LIST))

OBJS = $(SRCS_LIST:.c=.o)

# INCLUDES = -I $(INC_DIR) -I $(LIBFT_DIR)
# OPENGL_INCLUDES =  -I/usr/local/Cellar/glfw/3.3.2/include
# OPENGL_SOURCES =-framework OpenGl -framework Cocoa  -lglfw3 -framework CoreVideo -framework IOKit -lSOIL
CC = gcc
CFLAGS =
# CFLAGS = -Wall -Wextra -Werror -g

all: $(NAME)

%.o: %.c
	@$(CC) $(CFLAGS)  -o $@ -c $<
	@echo ".\c"

$(NAME): $(OBJS)
	@$(CC) $(CFLAGS) $(OBJS) -o $(NAME)
	@echo "$(NAME) executable created"

clean:
	@/bin/rm -f $(OBJS)
	@echo "Object files deleted"

fclean: clean
	@/bin/rm -f $(NAME)
	@echo "Executable files deleted"

re: fclean all
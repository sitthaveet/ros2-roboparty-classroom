FROM ros:humble-ros-base-jammy
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-rviz2 ros-humble-robot-state-publisher ros-humble-joint-state-publisher-gui \
    ros-humble-example-interfaces python3-colcon-common-extensions \
    xvfb x11vnc novnc websockify openbox supervisor \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/ros2_ws
COPY ros2_ws/src ./src
RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install
COPY docker/supervisord.conf /etc/classroom/supervisord.conf
# Every `docker compose exec ros bash` shell starts with ROS and the workspace sourced.
RUN echo "source /opt/ros2_ws/install/setup.bash; PS1='ROS2 classroom> '" >> /root/.bashrc
ENV DISPLAY=:1 LIBGL_ALWAYS_SOFTWARE=1 ROS_LOCALHOST_ONLY=1
EXPOSE 6080
CMD ["bash", "-c", "source /opt/ros2_ws/install/setup.bash && exec supervisord -c /etc/classroom/supervisord.conf"]

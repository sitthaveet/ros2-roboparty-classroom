FROM ros:humble-ros-base-jammy
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-rviz2 ros-humble-robot-state-publisher ros-humble-joint-state-publisher-gui \
    ros-humble-example-interfaces ros-humble-tf2-ros python3-colcon-common-extensions \
    xvfb x11vnc novnc websockify openbox supervisor xterm mesa-utils scrot \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/ros2_ws
COPY ros2_ws/src ./src
RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install
COPY docker /etc/classroom
COPY scripts ./scripts
COPY tests ./tests
RUN chmod +x /etc/classroom/*.sh /opt/ros2_ws/scripts/*.sh \
    && printf '\nsource /etc/classroom/entrypoint-rc.sh\n' >> /root/.bashrc
ENV DISPLAY=:1 LIBGL_ALWAYS_SOFTWARE=1 ROS_LOCALHOST_ONLY=1
EXPOSE 6080
ENTRYPOINT ["/etc/classroom/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/classroom/supervisord.conf"]

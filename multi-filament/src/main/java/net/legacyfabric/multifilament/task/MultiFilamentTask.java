package net.legacyfabric.multifilament.task;

import org.gradle.api.DefaultTask;

import javax.inject.Inject;

public abstract class MultiFilamentTask extends DefaultTask {
	@Inject
	public MultiFilamentTask() {
		this.setGroup("multi-filament");
	}
}

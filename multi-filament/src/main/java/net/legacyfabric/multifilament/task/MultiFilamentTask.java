package net.legacyfabric.multifilament.task;

import javax.inject.Inject;

import org.gradle.api.DefaultTask;

public abstract class MultiFilamentTask extends DefaultTask {
	@Inject
	public MultiFilamentTask() {
		this.setGroup("multi-filament");
	}
}
